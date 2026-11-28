"""Tests for dronemsg.py. Run: cd software/protocol && python -m unittest -v test_dronemsg"""
import json, os, unittest
import dronemsg as M

HERE = os.path.dirname(os.path.abspath(__file__))


class MO(unittest.TestCase):
    def test_report_only_is_51_bytes(self):
        self.assertEqual(len(M.encode_mo(1, 0, M.VEC_REPORT)), 51)

    def test_round_trip(self):
        jpg = b"\xff\xd8" + os.urandom(9000) + b"\xff\xd9"
        b = M.encode_mo(1, 70000, M.VEC_REPORT, [M.ack_section(7, 3, 1), M.photo_section(5, 0, 1, len(jpg), jpg),
                                                 M.text_section(M.SEC_DIAG, "a=1;b=two"), M.text_section(M.SEC_LOG, "hello")])
        d = M.decode_mo(b)
        self.assertEqual(d["session"], 70000 & 0xFFFF)
        r = d["report"]
        for k in M.REPORT_FIELDS: self.assertEqual(r[k], M.VEC_REPORT[k], k)
        self.assertAlmostEqual(r["lat_deg"], 49.70); self.assertEqual(r["mode_name"], "station")
        self.assertEqual(r["fault_names"], ["camera", "modem_retry"])
        self.assertEqual(d["acks"], [dict(seq=7, result="bad_value", index=1)])
        self.assertEqual(d["photos"][0]["data"], jpg)
        self.assertEqual(d["diag"], [dict(a="1", b="two")]); self.assertEqual(d["log"], ["hello"])

    def test_crc_catches_a_flipped_bit(self):
        b = bytearray(M.encode_mo(1, 1, M.VEC_REPORT)); b[10] ^= 4
        with self.assertRaises(M.ProtocolError): M.decode_mo(bytes(b))

    def test_truncated(self):
        with self.assertRaises(M.ProtocolError): M.decode_mo(b"\xd1\x01")


class MT(unittest.TestCase):
    K = bytes(range(32))

    def test_round_trip(self):
        b = M.encode_mt(self.K, 1, 8, 1840000100, M.VEC_COMMANDS)
        d = M.decode_mt(self.K, b, boat_id=1, last_seq=7)
        self.assertEqual(d["seq"], 8)
        names = [c[0] for c in d["commands"]]
        self.assertEqual(names, ["HOLD", "SET_REPORT", "SET_ROUTE", "PHOTO", "MODE"])
        hold = d["commands"][0][1]
        self.assertAlmostEqual(hold["lat"], 18.1022); self.assertAlmostEqual(hold["lon"], -64.4051); self.assertEqual(hold["radius_m"], 1000)
        self.assertEqual(len(d["commands"][2][1]["points"]), 3)

    def test_rejections(self):
        b = M.encode_mt(self.K, 1, 8, 0, [("DIAG", {})])
        for args, why in (((bytes(32), b), "bad_signature"), ((self.K, b, 1, 8), "old_sequence"), ((self.K, b, 2), "wrong_boat")):
            with self.assertRaises(M.ProtocolError) as e: M.decode_mt(*args)
            self.assertEqual(str(e.exception), why)
        t = bytearray(b); t[11] ^= 1
        with self.assertRaises(M.ProtocolError): M.decode_mt(self.K, bytes(t))

    def test_range_checks(self):
        for name, a in (("SET_REPORT", dict(minutes=10)), ("HOLD", dict(lat=18, lon=-64, radius_m=50)),
                        ("SET_ROUTE", dict(points=[])), ("PHOTO", dict(kind=1, max_bytes=500000)), ("MODE", dict(mode=5))):
            with self.assertRaises(M.ProtocolError): M.encode_mt(self.K, 1, 1, 0, [(name, a)])


class Vectors(unittest.TestCase):
    def test_vectors_file_is_current(self):
        with open(os.path.join(HERE, "vectors.json")) as f: v = json.load(f)
        self.assertEqual(v, json.loads(json.dumps(M.vectors())), "run: python dronemsg.py --vectors")


if __name__ == "__main__":
    unittest.main()
