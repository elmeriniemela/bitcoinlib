# -*- coding: utf-8 -*-
#
#    bitcoinlib - Compact Python Bitcoin Library
#    Unit Tests for Key, Encoding and Mnemonic Class
#    © 2017 March - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import unittest
import json

from bitcoinlib.keys import *

# Number of bulktests for generation of private, public keys and hdkeys. Set to 0 to disable
# WARNING: Can be slow for a larger number of tests
BULKTESTCOUNT = 10


class TestPrivateKeyConversions(unittest.TestCase):

    def setUp(self):
        self.privatekey_hex = 'b954f71933986e3de76d3a94454dc52ec082c662ba67ca3ba48ff72bc2704a58'
        self.k = Key(self.privatekey_hex, compressed=True)
        self.ku = Key(self.privatekey_hex, compressed=False)

    def test_private_key_conversions_dec(self):
        self.assertEqual(83827997552125623280808720137320612316470870230953489181279239295529837939288,
                         self.k.private_dec())

    def test_private_key_conversions_hex(self):
        self.assertEqual('b954f71933986e3de76d3a94454dc52ec082c662ba67ca3ba48ff72bc2704a58', self.k.private_hex())

    def test_private_key_conversions_wif_uncompressed(self):
        self.assertEqual('5KDudqswBNJ8mf2k7Gxn72UknDBh7GFjj9NGJrY22SY1hjKS1gF', self.ku.wif())

    def test_private_key_conversions_wif(self):
        self.assertEqual('L3RyKcjp8kzdJ6rhGhTC5bXWEYnC2eL3b1vrZoduXMht6m9MQeHy', self.k.wif())

    def test_private_key_public(self):
        self.assertEqual('034781e448a7ff0e1b66f1a249b4c952dae33326cf57c0a643738886f4efcd14d5', self.k.public())

    def test_private_key_public_uncompressed(self):
        self.assertEqual('044781e448a7ff0e1b66f1a249b4c952dae33326cf57c0a643738886f4efcd14d57a380bc32c26f46e733c'
                         'd991064c2e7f7d532b9c9ca825671a8809ab6876c78b', self.ku.public_uncompressed())


class TestPrivateKeyImport(unittest.TestCase):

    def test_private_key_import_key(self):
        self.k = Key(61876261089097932796193024729035977913579848833009517639587741086858579422075)
        self.assertEqual('L1odb1uUozbfK2NrsMyhJfvRsxGM2AxixgPL8vG9BUBnE6W1VyTX', self.k.wif())

    def test_private_key_import_key_str(self):
        self.k = Key('61876261089097932796193024729035977913579848833009517639587741086858579422075')
        self.assertEqual('L1odb1uUozbfK2NrsMyhJfvRsxGM2AxixgPL8vG9BUBnE6W1VyTX', self.k.wif())

    def test_private_key_import_key_hex_compressed(self):
        self.k = Key('1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD01')
        self.assertEqual('KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ', self.k.wif())

    def test_private_key_import_key_byte(self):
        pk = b':\xbaAb\xc7%\x1c\x89\x12\x07\xb7G\x84\x05Q\xa7\x199\xb0\xde\x08\x1f\x85\xc4\xe4L\xf7\xc1>A\xda\xa6\x01'
        self.k = Key(pk)
        self.assertEqual('KyBsPXxTuVD82av65KZkrGrWi5qLMah5SdNq6uftawDbgKa2wv6S', self.k.wif())

    def test_private_key_import_key_bytearray(self):
        pk = bytearray(b':\xbaAb\xc7%\x1c\x89\x12\x07\xb7G\x84\x05Q\xa7\x199\xb0\xde\x08\x1f\x85\xc4\xe4L\xf7\xc1>'
                       b'A\xda\xa6\x01')
        self.k = Key(pk)
        self.assertEqual('KyBsPXxTuVD82av65KZkrGrWi5qLMah5SdNq6uftawDbgKa2wv6S', self.k.wif())

    def test_private_key_import_wif(self):
        self.k = Key('L1odb1uUozbfK2NrsMyhJfvRsxGM2AxixgPL8vG9BUBnE6W1VyTX')
        self.assertEqual('88ccb90221d9b44df8dd317307de2d6019c9c7448dccaa1e45bae77e5a022b7b', self.k.private_hex())

    def test_private_key_import_wif_uncompressed(self):
        self.k = Key('5KJvsngHeMpm884wtkJNzQGaCErckhHJBGFsvd3VyK5qMZXj3hS')
        self.assertFalse(self.k.compressed)
        self.assertEqual('c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a', self.k.private_hex())

    def test_private_key_import_generate_random(self):
        self.k = Key()
        self.assertIn(self.k.wif()[0], ['K', 'L'])
        self.assertEqual(52, len(self.k.wif()))

    def test_private_key_import_error_1(self):
        self.assertRaisesRegexp(BKeyError, "Invalid checksum, not a valid WIF key",
                                Key, 'L1odb1uUozbfK2NrsMyhJfvRsxGM2axixgPL8vG9BUBnE6W1VyTX')

    def test_private_key_import_error_2(self):
        self.assertRaisesRegexp(BKeyError, "Unrecognised key format",
                                Key, 'M1odb1uUozbfK2NrsMyhJfvRsxGM2AxixgPL8vG9BUBnE6W1VyTX')

    def test_private_key_import_testnet(self):
        self.k = Key('92Pg46rUhgTT7romnV7iGW6W1gbGdeezqdbJCzShkCsYNzyyNcc', 'testnet')
        self.assertEqual('92Pg46rUhgTT7romnV7iGW6W1gbGdeezqdbJCzShkCsYNzyyNcc', self.k.wif())
        self.assertEqual('mipcBbFg9gMiCh81Kj8tqqdgoZub1ZJRfn', self.k.address())


class TestPublicKeyConversion(unittest.TestCase):

    def setUp(self):
        self.publickey_hex = '044781e448a7ff0e1b66f1a249b4c952dae33326cf57c0a643738886f4efcd14d57a380bc32c26f46e733cd' \
                             '991064c2e7f7d532b9c9ca825671a8809ab6876c78b'
        self.K = Key(self.publickey_hex)
        self.KC = Key('034781e448a7ff0e1b66f1a249b4c952dae33326cf57c0a643738886f4efcd14d5')

    def test_public_key_get_address_uncompressed(self):
        self.assertEqual('12ooWDQp6mujkVpEWHdfHmfM4rU17bokWw', self.K.address_uncompressed())

    def test_public_key_get_address(self):
        self.assertEqual('1P2X35YnajqoBXtPpQXJzV1QMnqSZQsn82', self.KC.address())

    def test_public_key_get_point(self):
        self.assertEqual((32343711077743629729728681292399790965391040816412086995020432364076041835733,
                          55281192143835269607479311758661973079027103826274522268778194868406595274635),
                         self.K.public_point())

    def test_public_key_get_hash160_uncompressed(self):
        self.assertEqual('13d21450578cd8f8645d2e56e684deb7cd77864b', self.K.hash160())

    def test_public_key_get_hash160(self):
        self.assertEqual('f19c417fd97e364afb06e1edd2c0e6a7ecf1af00', self.KC.hash160())

    def test_public_key_try_private(self):
        self.assertFalse(self.K.private_hex())

    def test_public_key_import_error(self):
        self.assertRaisesRegexp(BKeyError, "Unrecognised key format",
                                Key, ['064781e448a7ff0e1b66f1a249b4c952dae33326cf57c0a643738886f4efcd14d5', 'public'])


class TestPublicKeyUncompressed(unittest.TestCase):

    def setUp(self):
        self.K = Key('025c0de3b9c8ab18dd04e3511243ec2952002dbfadc864b9628910169d9b9b00ec')

    def test_public_key_point(self):
        self.assertEqual((41637322786646325214887832269588396900663353932545912953362782457239403430124,
                          16388935128781238405526710466724741593761085120864331449066658622400339362166),
                         self.K.public_point(),)

    def test_public_key_uncompressed(self):
        self.assertEqual('045c0de3b9c8ab18dd04e3511243ec2952002dbfadc864b9628910169d9b9b00ec243bcefdd4347074d4'
                         '4bd7356d6a53c495737dd96295e2a9374bf5f02ebfc176',
                         self.K.public_uncompressed())

    def test_public_key_address_uncompressed(self):
        self.assertEqual('1thMirt546nngXqyPEz532S8fLwbozud8', self.K.address_uncompressed())


class TestHDKeysImport(unittest.TestCase):

    def setUp(self):
        self.k = HDKey.from_seed('000102030405060708090a0b0c0d0e0f')
        self.k2 = HDKey.from_seed('fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a878'
                                  '4817e7b7875726f6c696663605d5a5754514e4b484542')
        self.xpub = HDKey('xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqse'
                          'fD265TMg7usUDFdp6W1EGMcet8')

    def test_hdkey_import_seed_1(self):

        self.assertEqual('xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TG'
                         'tRBeJgk33yuGBxrMPHi', self.k.extended_wif())
        self.assertEqual('xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TM'
                         'g7usUDFdp6W1EGMcet8', self.k.extended_wif(public=True))

    def test_hdkey_import_seed_2(self):
        self.assertEqual('xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3L'
                         'qFtT2emdEXVYsCzC2U', self.k2.extended_wif())
        self.assertEqual('xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJ'
                         'Y47LJhkJ8UB7WEGuduB', self.k2.extended_wif_public())

    def test_hdkey_random(self):
        self.k = HDKey()
        self.assertEqual('xprv', self.k.extended_wif()[:4])
        self.assertEqual(111, len(self.k.extended_wif()))

    def test_hdkey_import_extended_private_key(self):
        extkey = 'xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4m' \
                 'LTj34bhnZX7UiM'
        self.k = HDKey(extkey)
        self.assertEqual(extkey, self.k.extended_wif())

    def test_hdkey_import_extended_public_key(self):
        extkey = 'xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7' \
                 'DogT5Uv6fcLW5'
        self.k = HDKey(extkey)
        self.assertEqual(extkey, self.k.extended_wif())

    def test_hdkey_import_simple_key(self):
        self.k = HDKey('L45TpiVN3C8Q3MoosGDzug1acpnFjysseBLVboszztmEyotdSJ9g')
        self.assertEqual(
            'xprv9s21ZrQH143K24Mfq5zL5MhWK9hUhhGbd45hLXo2Pq2oqzMMo63oStZzFAbeoRRpMHE67jGmBQKCr2YovK2G23x5uzaztRbEW9pc'
            'j6SqMFd', self.k.extended_wif())

    def test_hdkey_import_bip38_key(self):
        self.k = HDKey('6PYNKZ1EAgYgmQfmNVamxyXVWHzK5s6DGhwP4J5o44cvXdoY7sRzhtpUeo',
                       passphrase='TestingOneTwoThree')
        self.assertEqual('L44B5gGEpqEDRS9vVPz7QT35jcBG2r3CZwSwQ4fCewXAhAhqGVpP', self.k.private().wif())

    def test_hdkey_import_public(self):
        self.assertEqual('15mKKb2eos1hWa6tisdPwwDC1a5J1y9nma', self.xpub.public().address())
        self.assertEqual('0339a36013301597daef41fbe593a02cc513d0b55527ec2df1050e2e8ff49c85c2',
                         self.xpub.public().public_hex())

    def test_hdkey_import_public_try_private(self):
        self.assertFalse(self.xpub.public().wif())
        self.assertFalse(self.xpub.public().private_hex())
        self.assertFalse(self.xpub.public().private_byte())


class TestHDKeysChildKeyDerivation(unittest.TestCase):

    def setUp(self):
        self.k = HDKey.from_seed('000102030405060708090a0b0c0d0e0f')
        self.k2 = HDKey.from_seed('fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8'
                                  '784817e7b7875726f6c696663605d5a5754514e4b484542')

    def test_hdkey_path_m_0h(self):
        self.assertEqual('xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7'
                         'XnxHrnYeSvkzY7d2bhkJ7', self.k.subkey_for_path('m/0H').extended_wif())
        self.assertEqual('xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9x'
                         'v5ski8PX9rL2dZXvgGDnw', self.k.subkey_for_path('m/0H').extended_wif(public=True))

    def test_hdkey_path_m_0h_1(self):
        self.assertEqual('xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H'
                         '2EU4pWcQDnRnrVA1xe8fs', self.k.subkey_for_path('m/0H/1').extended_wif())
        self.assertEqual('xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqc'
                         'k2AxYysAA7xmALppuCkwQ', self.k.subkey_for_path('m/0H/1').extended_wif(public=True))

    def test_hdkey_path_m_0h_1_2h(self):
        self.assertEqual('xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjAN'
                         'TtpgP4mLTj34bhnZX7UiM', self.k.subkey_for_path('m/0h/1/2h').extended_wif())
        self.assertEqual('xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4'
                         'trkrX7x7DogT5Uv6fcLW5', self.k.subkey_for_path('m/0h/1/2h').extended_wif(public=True))

    def test_hdkey_path_m_0h_1_2h_1000000000(self):
        self.assertEqual('xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUi'
                         'hUZREPSL39UNdE3BBDu76', self.k.subkey_for_path('m/0h/1/2h/2/1000000000').extended_wif())
        self.assertEqual('xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTv'
                         'XEYBVPamhGW6cFJodrTHy',
                         self.k.subkey_for_path('m/0h/1/2h/2/1000000000').extended_wif_public())

    def test_hdkey_path_key2(self):
        self.k2.info()
        self.assertEqual('xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEc'
                         'BYJUuekgW4BYPJcr9E7j',
                         self.k2.subkey_for_path('m/0/2147483647h/1/2147483646h/2').extended_wif())
        self.assertEqual('xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb'
                         '9rXpVGyy3bdW6EEgAtqt',
                         self.k2.subkey_for_path('m/0/2147483647h/1/2147483646h/2').extended_wif_public())

    def test_hdkey_path_invalid(self):
        with self.assertRaises(BKeyError):
            self.k2.subkey_for_path('m/0/').extended_wif()

    def test_hdkey_path_invalid2(self):
        with self.assertRaises(BKeyError):
            self.k2.subkey_for_path('m/-1').extended_wif()


class TestHDKeysPublicChildKeyDerivation(unittest.TestCase):

    def setUp(self):
        self.K = HDKey('xpub6ASuArnXKPbfEVRpCesNx4P939HDXENHkksgxsVG1yNp9958A33qYoPiTN9QrJmWFa2jNLdK84bWmyqTSPGtApP8P'
                       '7nHUYwxHPhqmzUyeFG')
        self.k = HDKey('xprv9wTYmMFdV23N21MM6dLNavSQV7Sj7meSPXx6AV5eTdqqGLjycVjb115Ec5LgRAXscPZgy5G4jQ9csyyZLN3PZLxoM'
                       '1h3BoPuEJzsgeypdKj')

    def test_hdkey_derive_public_child_key(self):
        self.assertEqual('1BvgsfsZQVtkLS69NvGF8rw6NZW2ShJQHr', self.K.child_public(0).public().address())

    def test_hdkey_derive_public_child_key2(self):
        self.assertEqual('17JbSP83rPWmbdcdtiiTNqBE8MgGN8kmUk', self.K.child_public(8).public().address())

    def test_hdkey_private_key(self):
        self.assertEqual('KxABnXp7SiuWi218c14KkjEMV7SjcfXnvsWaveNVxWZU1Rwi8zNQ',
                         self.k.child_private(7).private().wif())

    def test_hdkey_private_key_hardened(self):
        self.k2 = HDKey('xprv9s21ZrQH143K31AgNK5pyVvW23gHnkBq2wh5aEk6g1s496M8ZMjxncCKZKgb5j'
                        'ZoY5eSJMJ2Vbyvi2hbmQnCuHBujZ2WXGTux1X2k9Krdtq')
        self.assertEqual('xprv9wTErTSu5AWGkDeUPmqBcbZWX1xq85ZNX9iQRQW9DXwygFp7iRGJo79dsVctcsCHsnZ3XU3DhsuaGZbDh8iDkB'
                         'N45k67UKsJUXM1JfRCdn1', str(self.k2.subkey_for_path('3/2H')))


class TestHDKeysTestnet(unittest.TestCase):

    def test_hdkey_testnet_random(self):
        self.k = HDKey(network='testnet')

        self.assertEqual('tprv', self.k.extended_wif()[:4])
        self.assertEqual('tpub', self.k.extended_wif_public()[:4])
        self.assertIn(self.k.public().address()[:1], ['m', 'n'])

    def test_hdkey_testnet_import(self):
        self.k = HDKey('tprv8ZgxMBicQKsPf2S18qpSypHPZBK7mdiwvXHPh5TSjGjm2pLacP4tEqVjLVyagTLLgSZK4YyBNb4eytBykE755Kc'
                       'L9YXAqPtfERNRfwRt54M')

        self.assertEqual('cPSokRrLueavzAmVBmAXwgALkumRNMN9pErvRLAXvx58NBJAkEYJ', self.k.private().wif())
        self.assertEqual('tpubD6NzVbkrYhZ4YVTo2VV3PDwW8Cq3vxurVptAybVk9YY9sJbMEmtURL7bWgKxXSWSahXu6HbHkdpjBGzwYYkJm'
                         'u2VmoeHuiTmzHZpJo8Cdpb', self.k.extended_wif_public())
        self.assertEqual('n4c8TKkqUmj3b8VJrTioiZuciyaCDRd6iE', self.k.public().address())


class TestBip38(unittest.TestCase):

    def setUp(self):
        workdir = os.path.dirname(__file__)
        with open('%s/%s' % (workdir, 'bip38_protected_key_tests.json'), 'r') as f:
            self.vectors = json.load(f)

    def test_encrypt_private_key(self):
        for v in self.vectors["valid"]:
            k = Key(v['wif'])
            print("Check %s + %s = %s " % (v['wif'], v['passphrase'], v['bip38']))
            self.assertEqual(str(v['bip38']), k.bip38_encrypt(str(v['passphrase'])))

    def test_decrypt_bip38_key(self):
        for v in self.vectors["valid"]:
            k = Key(v['bip38'], passphrase=str(v['passphrase']))
            print("Check %s - %s = %s " % (v['bip38'], v['passphrase'], v['wif']))
            self.assertEqual(str(v['wif']), k.wif())

    def test_bip38_invalid_keys(self):
        for v in self.vectors["invalid"]["verify"]:
            print("Checking invalid key %s" % v['base58'])
            self.assertRaisesRegexp(BKeyError, "Unrecognised key format", Key, [str(v['base58'])])


class TestKeysBulk(unittest.TestCase):
    """
    Test Child Key Derivation

    Use the 2 different methods to derive child keys. One through derivation from public parent,
    and one thought private parent. They should be the same.
    """

    def setUp(self):
        self.K = HDKey('xpub6ASuArnXKPbfEVRpCesNx4P939HDXENHkksgxsVG1yNp9958A33qYoPiTN9QrJmWFa2jNLdK84bWmyqTSPGtApP8P'
                       '7nHUYwxHPhqmzUyeFG')
        self.k = HDKey('xprv9wTYmMFdV23N21MM6dLNavSQV7Sj7meSPXx6AV5eTdqqGLjycVjb115Ec5LgRAXscPZgy5G4jQ9csyyZLN3PZLxoM'
                       '1h3BoPuEJzsgeypdKj')

    def test_hdkey_derive_from_public_and_private_index(self):
        global BULKTESTCOUNT
        if not BULKTESTCOUNT:
            self.skipTest("Skip bulktesting. Bulktestcount == 0")
        for i in range(BULKTESTCOUNT):
            pub_with_pubparent = self.K.child_public(i).public().address()
            pub_with_privparent = self.k.child_private(i).public().address()
            if pub_with_privparent != pub_with_pubparent:
                print("Error index %4d: pub-child %s, priv-child %s" % (i, pub_with_privparent, pub_with_pubparent))
            self.assertEqual(pub_with_pubparent, pub_with_privparent)

    def test_hdkey_derive_from_public_and_private_random(self):
        global BULKTESTCOUNT
        if not BULKTESTCOUNT:
            self.skipTest("Skip bulktesting. Bulktestcount == 0")
        for i in range(BULKTESTCOUNT):
            k = HDKey()
            K = HDKey(k.extended_wif_public())
            pub_with_pubparent = K.child_public().public().address()
            pub_with_privparent = k.child_private().public().address()
            if pub_with_privparent != pub_with_pubparent:
                print("Error random key: %4d: pub-child %s, priv-child %s" %
                      (i, pub_with_privparent, pub_with_pubparent))
            self.assertEqual(pub_with_pubparent, pub_with_privparent)


if __name__ == '__main__':
    unittest.main()
