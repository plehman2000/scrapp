from diffusers import DiffusionPipeline
from PIL import Image
# pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-dev")

# prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell")

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]



image.save("bruh.png")