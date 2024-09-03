import torch
from PIL import Image
from lavis.models import load_model_and_preprocess
# setup device to use
device = torch.device("cuda:0") if torch.cuda.is_available() else "cpu"
# load sample image
raw_image = Image.open("/home/zhang/workspace/yinxu/LoHo-Ravens/0.png").convert("RGB")
# loads InstructBLIP model
model, vis_processors, _ = load_model_and_preprocess(name="blip2_vicuna_instruct", model_type="vicuna7b", is_eval=True, device=device)
# prepare the image
image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
print(model.generate({"image": image, "prompt": "what are the colors of the blocks on the table?"}))