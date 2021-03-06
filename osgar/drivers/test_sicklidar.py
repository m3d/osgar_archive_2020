import unittest
from unittest.mock import MagicMock

from osgar.drivers.sicklidar import SICKLidar
from osgar.bus import Bus


class SICKLidarTest(unittest.TestCase):

    def test_start_stop(self):
        config = {}
        logger = MagicMock()
        bus = Bus(logger)
        lidar = SICKLidar(config, bus=bus.handle('lidar'))
        lidar.start()
        lidar.request_stop()
        lidar.join()

    def test_parse_raw_data(self):
        raw_data = b"""\x02sRA LMDscandata 1 1 10A719E 0 0 20F9 20FB 26C0C24A 26C0DDF1 0 0 1 0 0 5DC
A2 0 1 DIST1 3F800000 00000000 FFF92230 D05 32B 87B 88D 8A8 8C3 8DE 8F5 912 936
95F 986 9B8 9D4 9EA 9FA A07 A16 A29 A38 A48 A58 A69 A7A A8B A9A AB1 0 0 0 0 0 0
0 0 0 1E 635 66A 6A6 6DB D7B DC5 E0E E60 EB4 EFC F55 FAE 1008 106E 10D1 113C 11C
4 1255 12C0 12CA 12BF 12B8 12A9 129C 1294 128A 1279 1271 1267 125E 1253 124B 124
3 607 61B 60D 604 5FB 5F5 5EC 5EC 5EF 5F0 5F1 5F4 5F8 603 60D 61F 625 62A 653 1F
31 1F84 202E 2060 2082 210B 21DA 228D 2345 23E1 249E 253A 261E 26ED 27BE 28B4 29
49 2957 294D 294D 2946 2944 2936 2937 2935 292E 11D8 B1B B10 B00 AE8 AD0 AC8 ABD
 AA4 A9B A93 A8C A88 A88 A83 A7D A6F A5F A4D A44 A3C A37 A31 A2C A32 A33 A33 0 6
D4 6C9 6C3 6B9 6B0 6AC 6AD 6AE 6A7 6A2 69C 69D 69C 67 88 D6 147 1A8 1C4 1C9 1C9
1C7 1C8 1C9 1CC 1CA 1CB 1CC 1C6 1CD 1CB 1CF 1D1 1CF 1D0 1CE 1D5 1CF 1D1 1D5 1D4
1D9 1D8 1D8 1D7 1D9 1D9 1D6 1C9 18D 156 126 111 10A 104 100 F9 EA E8 E5 E1 E4 E3
 EF 123 17F 1D0 1EC 1F4 1F7 1FA 1F9 1FC 200 1FF 206 205 204 20D 20C 20C 20A 20F
210 212 210 216 213 219 219 21C 222 221 222 21E 21F 21C 21A 216 219 211 213 210
211 211 212 216 257 282 28B 291 292 296 2A6 2B2 2C2 2BD 2B5 2A4 2A9 2A6 299 299
291 292 28E 290 280 27C 27A 270 272 26A 26D 263 262 255 24F 24B 245 240 234 234
227 22B 21E 220 21F 217 216 21D 211 20D 207 200 1F9 1FA 1EF 1EC 1E5 1E3 1E4 1DE
1DA 1D7 1CD 1CF 1D0 1C6 1D0 1C3 1BE 1C0 1B7 1B7 1BB 1B8 1B7 1B2 1B3 1AD 1AF 1B3
1B4 1AE 1B0 1B0 1AF 1A8 1AF 1AD 1AB 1AD 1AC 1AB 1AB 1A5 1A2 1B2 1AE 1B4 1B8 1B0
1B0 1A9 1B3 1B1 1B2 1AE 1B8 1BC 1B7 1B4 1B8 1C3 1C4 1CD 1CC 1CD 1CC 1D7 20E AFA
0 0 0 0 4A6 4A6 4A5 4A4 49C 49A 498 49C 498 499 496 493 48F 48D 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 482 484 482 0 0 0 49A 4A0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
2 14 1F 24 28 34 35 3C 40 45 49 4B 4D 50 50 50 50 51 55 55 54 51 54 51 50 51 54
54 52 52 54 55 54 52 56 57 55 55 58 58 58 59 59 58 56 59 57 58 57 59 5C 5A 59 5B
 5B 58 5C 5C 5C 5A 5E 5B 5E 60 5F 5C 5C 5B 5B 5A 5A 5D 5B 5B 5D 5D 5D 5C 5B 5E 5
F 5D 63 5F 62 5E 63 61 63 64 61 62 68 68 67 62 66 65 6B 6A 6A 66 67 6C 6C 6D 6D
6C 6F 6D 6D 6E 6C 72 70 71 71 73 75 75 77 77 75 76 79 76 78 77 79 7A 7D 7E 7D 7D
 80 81 82 82 83 84 82 83 83 86 88 8A 8B 87 8C 90 8E 8D 92 93 95 97 97 95 9A 9E 9
C A1 A2 A5 A6 A3 A8 AC B0 AE AE B2 B4 B6 B7 BA BF C1 C4 C0 CA CB C7 CA CC CB CE
D2 CE D6 D3 DA D7 D3 DF DC E3 E6 ED EC EF F3 FB FE FD 105 10D 112 117 11F 125 12
A 130 135 134 13D 138 134 131 131 12C 12A 128 128 126 11B 11C 113 11B 10E 2 2 2
2 2 2 184 18E 2 21E 211 213 229 247 244 26A 288 293 295 28C 290 28A 281 28D 28B
289 286 28C 290 28C 28B 28B 28B 287 28A 282 284 286 283 283 286 277 285 288 282
28A 282 281 277 271 256 2 10C F5 FA F0 F3 F4 EB F2 F2 F4 EC EB 2 2 2 2 2 2 0 2 2
 2 2 2 2 2 2 0 2 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
 2 2 2 2 2 2 2 2 2 2 11A 2 133 135 132 13E 147 14E 2 14F 5BB 562 555 55A 54C 549
 545 536 535 535 52D 522 51B 51A 519 50D 509 504 506 500 4FD 4FF 4E4 0 0 1 B not
 defined 0 0 0\x03"""

        data = SICKLidar.parse_raw_data(raw_data)
        self.assertIsNotNone(data)

    def test_sleep(self):
        config = {}
        logger = MagicMock()
        bus = Bus(logger)
        lidar = SICKLidar(config, bus=bus.handle('lidar'))
        self.assertIsNone(lidar.sleep)

        config = {"sleep": 0.1}
        lidar = SICKLidar(config, bus=bus.handle('lidar'))
        self.assertAlmostEqual(lidar.sleep, 0.1)

    def test_empty_scan(self):
        tcp_buf = b'\x02sRA LMDscandata 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\x03'
        data = SICKLidar.parse_raw_data(tcp_buf)
        self.assertEqual(data, ([], None))  # empty scan and no RSSI

        # TODO test that empty scan is not published!

    def test_mask(self):
        config = {
                'mask': [1, -1]
                }
        logger = MagicMock()
        bus = Bus(logger)
        lidar = SICKLidar(config, bus=bus.handle('lidar'))

        scan = [123] * 270
        masked_scan = lidar.apply_mask(scan)
        self.assertEqual(masked_scan[0], 0)
        self.assertEqual(scan[1:-1], masked_scan[1:-1])
        self.assertEqual(masked_scan[-1], 0)


    def test_blind_zone(self):
        config = {
                'blind_zone': 10
                }
        logger = MagicMock()
        bus = Bus(logger)
        lidar = SICKLidar(config, bus=bus.handle('lidar'))

        scan = [123] * 269 + [2]
        masked_scan = lidar.apply_mask(scan)
        self.assertEqual(masked_scan[-1], 0)

# vim: expandtab sw=4 ts=4
