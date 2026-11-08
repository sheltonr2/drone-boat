"""Batch quadric-error edge-collapse decimation (numpy + scipy). Keeps the mesh manifold
(link condition) and rejects collapses that flip faces. Error threshold in mm."""
import numpy as np
import scipy.sparse as sp

def _face_planes(v, f):
    n = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
    a = np.linalg.norm(n, axis=1, keepdims=True)
    n = n / np.maximum(a, 1e-12)
    d = -np.einsum('ij,ij->i', n, v[f[:, 0]])
    return np.c_[n, d], a[:, 0]

def _quadrics(v, f):
    p, area = _face_planes(v, f)
    K = np.einsum('fi,fj->fij', p, p) * area[:, None, None]
    Q = np.zeros((len(v), 4, 4))
    for k in range(3):
        np.add.at(Q, f[:, k], K)
    return Q

def decimate(v, f, max_err=0.03, iters=40, verbose=False):
    v = v.astype(np.float64).copy(); f = f.copy()
    for it in range(iters):
        nv = len(v)
        Q = _quadrics(v, f)
        e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
        e = np.unique(np.sort(e, 1), axis=0)
        a, b = e[:, 0], e[:, 1]
        Qe = Q[a] + Q[b]
        mid = (v[a] + v[b]) / 2
        # candidate positions: a, b, midpoint -> pick lowest cost
        cands = np.stack([v[a], v[b], mid], 1)                     # E,3,3
        h = np.concatenate([cands, np.ones(cands.shape[:2] + (1,))], 2)
        cost = np.einsum('eki,eij,ekj->ek', h, Qe, h)
        best = np.argmin(cost, 1)
        c = cost[np.arange(len(e)), best]
        pos = cands[np.arange(len(e)), best]
        ok = c < max_err**2 * 4
        if ok.sum() == 0:
            break
        # link condition: common neighbours must equal 2
        A = sp.coo_matrix((np.ones(2*len(e)), (np.r_[a, b], np.r_[b, a])), shape=(nv, nv)).tocsr()
        idx = np.nonzero(ok)[0]
        common = np.asarray(A[a[idx]].multiply(A[b[idx]]).sum(1)).ravel()
        ok[idx[common != 2]] = False
        idx = np.nonzero(ok)[0]
        idx = idx[np.argsort(c[idx])]
        # vertex-face incidence for flip checks
        vf = sp.coo_matrix((np.ones(3*len(f)), (f.ravel(), np.repeat(np.arange(len(f)), 3))), shape=(nv, len(f))).tocsr()
        fn = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
        locked_v = np.zeros(nv, bool)
        remap = np.arange(nv); newpos = v.copy()
        chosen = 0
        indptr, indices = vf.indptr, vf.indices
        Aptr, Aind = A.indptr, A.indices
        for i in idx:
            va, vb = a[i], b[i]
            if locked_v[va] or locked_v[vb]:
                continue
            fa = indices[indptr[va]:indptr[va+1]]; fb = indices[indptr[vb]:indptr[vb+1]]
            fs = np.union1d(fa, fb)
            F = f[fs]
            keep = ~((F == va).any(1) & (F == vb).any(1))
            F2 = F[keep]
            P = v[F2].copy()
            m = (F2 == va) | (F2 == vb)
            P[m] = pos[i]
            n2 = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
            n1 = fn[fs[keep]]
            l1 = np.linalg.norm(n1, axis=1); l2 = np.linalg.norm(n2, axis=1)
            if np.any(l2 < 1e-9) or np.any(np.einsum('ij,ij->i', n1, n2) < 0.5 * l1 * l2):
                continue
            remap[vb] = va; newpos[va] = pos[i]
            nb = np.union1d(Aind[Aptr[va]:Aptr[va+1]], Aind[Aptr[vb]:Aptr[vb+1]])
            locked_v[nb] = True; locked_v[va] = True; locked_v[vb] = True
            chosen += 1
        if chosen == 0:
            break
        v = newpos
        f = remap[f]
        f = f[(f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 2] != f[:, 0])]
        used = np.unique(f)
        rm = -np.ones(len(v), int); rm[used] = np.arange(len(used))
        v = v[used]; f = rm[f]
        if verbose:
            print(f"  iter {it}: collapsed {chosen}, faces {len(f)}", flush=True)
        if chosen < 0.002 * len(f):
            break
    return v, f
