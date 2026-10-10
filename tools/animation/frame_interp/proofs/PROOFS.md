# PROOFS — frame_interp (ffmpeg minterpolate)

## Verification
```json
{
  "tool": "ffmpeg minterpolate (fps=30, mi_mode=mci, mc_mode=aobmc, me_mode=bidir)",
  "input_keyframes": 4,
  "output_frames": 16,
  "expected_output_frames": 16,
  "count_ok": true,
  "centroid_x": [
    139.47,
    143.76,
    147.86,
    153.0,
    161.01,
    168.35,
    173.18,
    177.37,
    181.58,
    185.87,
    190.39,
    196.93,
    206.56,
    212.33,
    215.2,
    219.47
  ],
  "monotonic_x": true,
  "on_motion_path": true,
  "travel_span_px": 80.0,
  "travel_ok": true
}
```

## SHA-256

- `input_keys.mp4`: `678d3d83f3749e116e63b11f40c6d09e4b79fedef80fb7fe0254b55bef8469f0`
- `interpolated.mp4`: `3352b0d38f68cf31c894f708b798e2db66b40d60674de6021612d56137f33d16`
- `keyframe_1.png`: `83a96abc09322ef50a82948c702459af3c0ee7b00ddb9e78e6068781e71b6c32`
- `keyframe_2.png`: `4aab9448dcfcc391bd824741d7aeec62d6302214f235ba5231683df41bceb15e`
- `keyframe_3.png`: `5fd149ebda94b2c10b7cf11bac03a8673ba3d253dd5a886be151f81428feff0b`
- `keyframe_4.png`: `e220a705819346db7e0328b293160c3ece702c4d4668115c4b741364d1f47031`
- `out_01.png`: `846ef64bc2483a250a964a95a24b8664f848e4822dcf6dc2483d0d4ef47b047c`
- `out_02.png`: `8ac6c7098a651380c39735dafc41c51f05efa595c916e4665a47de3f20d8d8fd`
- `out_03.png`: `a3cc9ecd4b62af1314ddad7e10e1c23f6ac49ea9f95c32192dfe8b93066ddea2`
- `out_04.png`: `d11a462f9438ce0ba7f3f0c486cfc90bcdb7c7f6df0219b986e5368700448831`
- `out_05.png`: `3673d6753ecd71b7a55a617c61618c599412bc6d94fe40ce31051002d6422631`
- `out_06.png`: `9440d8e3ae5705216a4dae9a2302e9a828600ed0cdfd14dc32a42853ace3bca1`
- `out_07.png`: `501e92eabde4fb7442991a9969a09c43e09213ba7e0e83f0127644ce9bca67bd`
- `out_08.png`: `779547a03082e048aabe2c50a9a9ee0dc33c8db062dd8307263c837b6d75caf0`
- `out_09.png`: `83f84664f00d59c498ef172389c5ae7ebe5d0223ca8cf757165d2bae9a36e05c`
- `out_10.png`: `66937dde51fd7c9eb3abd06cd85036660a31e88c9002b0dd49add661b61250e9`
- `out_11.png`: `cf5eaea8c200a497d0a22724a7c15d157baaedd156b254d2c5b3fdaeb96ae575`
- `out_12.png`: `b155ded5089b37ed12aac53a667635de51e4d0520acbc2fe2773dae11e08c736`
- `out_13.png`: `71b9371b9103adc04df2a2874dc7595e36fdca5bf72fb31ce4f8279b1443d3b3`
- `out_14.png`: `30cfb5fb3fd9d3bf71787d56c2709738143ae204fbe01f6e1dd19dffe446525e`
- `out_15.png`: `01253fefb46ebac197f363fb49cde5cbc25ca703303c9ea742b0dc2a0d472333`
- `out_16.png`: `38355682bd11f19af08d8a55d69cc26016e8b020f5b640bb46b686bb9ab80300`
