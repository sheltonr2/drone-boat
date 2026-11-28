"""End-to-end test of the shore server with the fake boat. Run: cd software/shore && python -m unittest -v test_shore"""
import base64, json, os, shutil, sys, tempfile, threading, unittest, urllib.error, urllib.request
from http.server import ThreadingHTTPServer
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "protocol"))
import server as S, fake_boat as F, dronemsg as M  # noqa: E402

KEY = "00" * 16 + "11" * 16  # test key only


class Shore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.cfg = dict(boat_id=1, data_dir=cls.tmp, send=False, boat_key_hex=KEY, dashboard_password="pw", webhook_secret="hook123")
        cls.store = S.Store(cls.tmp); cls.cmds = S.Commands(cls.store, cls.cfg)
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), S.make_handler(cls.store, cls.cmds, cls.cfg))
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown(); cls.store.db.close(); shutil.rmtree(cls.tmp)

    def get(self, path, pw="pw"):
        req = urllib.request.Request(self.base + path, headers={"Authorization": "Basic " + base64.b64encode(f"x:{pw}".encode()).decode()})
        with urllib.request.urlopen(req, timeout=10) as r: return r.read()

    def test_1_reports_and_photo(self):
        F.main(["--url", self.base + "/cloudloop/hook123", "--reports", "6", "--photo-every", "3"])
        self.assertEqual(self.store.q("select count(*) from report")[0][0], 6)
        photos = self.store.q("select file, bytes from photo")
        self.assertEqual(len(photos), 2)
        self.assertTrue(self.get("/photo/" + photos[0][0]).startswith(b"\xff\xd8"))
        page = self.get("/").decode()
        self.assertIn("Last report", page); self.assertIn("<svg", page); self.assertIn("<img", page)
        self.assertEqual(len(json.loads(self.get("/api/reports.json"))), 6)

    def test_2_wrong_secret_and_password(self):
        with self.assertRaises(urllib.error.HTTPError) as e: F.post(self.base + "/cloudloop/wrong", {"message": ""})
        self.assertEqual(e.exception.code, 404)
        with self.assertRaises(urllib.error.HTTPError) as e: self.get("/", pw="nope")
        self.assertEqual(e.exception.code, 401)

    def test_3_bad_message_kept(self):
        r = F.post(self.base + "/cloudloop/hook123", {"message": base64.b64encode(b"\xd1junk").decode()})
        self.assertFalse(r["ok"])
        self.assertEqual(self.store.q("select count(*) from raw where ok=0")[0][0], 1)

    def test_4_command_signed_then_acknowledged(self):
        body = "name=HOLD&lat=18.1022&lon=-64.4051&radius_m=1000"
        req = urllib.request.Request(self.base + "/command", data=body.encode(), method="POST",
                                     headers={"Authorization": "Basic " + base64.b64encode(b"x:pw").decode()})
        urllib.request.urlopen(req, timeout=10).read()
        seq, hx, status = self.store.q("select seq, hex, status from command order by seq desc limit 1")[0]
        self.assertEqual(status, "dry run")
        d = M.decode_mt(bytes.fromhex(KEY), bytes.fromhex(hx), boat_id=1, last_seq=seq - 1)
        self.assertEqual(d["commands"][0][0], "HOLD")
        F.main(["--url", self.base + "/cloudloop/hook123", "--reports", "1", "--photo-every", "0", "--ack", str(seq)])
        self.assertEqual(self.store.q("select status from command where seq=?", (seq,))[0][0], "applied")

    def test_5_out_of_range_command_refused(self):
        with self.assertRaises(M.ProtocolError): self.cmds.queue([("SET_REPORT", dict(minutes=5))])


if __name__ == "__main__":
    unittest.main()
