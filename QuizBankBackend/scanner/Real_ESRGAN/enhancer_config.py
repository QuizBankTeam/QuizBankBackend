class RealESRGANConfig:
    def __init__(self,
                 input='inputs',
                 model_name='RealESRGAN_x4plus_anime_6B',
                 output='results',
                 denoise_strength=0.5,
                 outscale=1,
                 model_path=None,
                 tile=0,
                 tile_pad=10,
                 pre_pad=10,
                 fp32=True,
                 alpha_upsampler='realesrgan',
                 ext='auto',
                 gpu_id=None):
        self.input = input
        self.model_name = model_name
        self.output = output
        self.denoise_strength = denoise_strength
        self.outscale = outscale
        self.model_path = model_path
        self.tile = tile
        self.tile_pad = tile_pad
        self.pre_pad = pre_pad
        self.fp32 = fp32
        self.alpha_upsampler = alpha_upsampler
        self.ext = ext
        self.gpu_id = gpu_id