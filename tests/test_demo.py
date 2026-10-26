import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from paper2.adapters import DemoHMACAdapter, DemoKEM, DemoAEAD
from paper2.protocol import HostNetwork

class DemoTests(unittest.TestCase):
    def test_hmac_demo_tamper(self):
        a=DemoHMACAdapter(b"test secret")
        sig=a.sign(b"message")
        self.assertTrue(a.verify(b"message",sig))
        self.assertFalse(a.verify(b"changed",sig))
    def test_demo_kem(self):
        secret=b"x"*32
        ct, ss=DemoKEM.encapsulate(secret)
        self.assertEqual(DemoKEM.decapsulate(ct,secret),ss)
    def test_demo_envelope_tamper(self):
        hn=HostNetwork(); key,_=hn.establish_demo_session()
        nonce, env=hn.encrypt_demo_message(key,b"payload")
        self.assertEqual(hn.decrypt_demo_message(key,nonce,env),b"payload")
        bad=env[:-1]+bytes([env[-1]^1])
        with self.assertRaises(ValueError): hn.decrypt_demo_message(key,nonce,bad)

if __name__=="__main__": unittest.main()
