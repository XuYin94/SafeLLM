import transformers
import torch
model_id = "meta-llama/Meta-Llama-3-8B-Instruct"

pipeline = transformers.pipeline(
  "text-generation",
  model="/mnt/bear1/users/zhangkang/yinxu/LLM_models/Meta-Llama-3-8B-Instruct/",
  model_kwargs={"torch_dtype": torch.bfloat16},
  device_map="auto",
)

messages = [
{"role": "system", "content": "You are a pirate chatbot who always responds in pirate speak!"},
{"role": "user", "content": "Who are you?"},
]

prompt = pipeline.tokenizer.apply_chat_template(
        messages, 
        tokenize=False, 
        add_generation_prompt=True,
)

terminators = [
    pipeline.tokenizer.eos_token_id,
    pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
]
pipeline.tokenizer.pad_token_id = pipeline.model.config.eos_token_id
outputs = pipeline(
    54*[prompt],
    max_new_tokens=2048,
    eos_token_id=terminators,
    do_sample=True,
    temperature=1.,
    top_p=0.9,
    batch_size=54,
    log_probs=True
    
)
print(outputs[0])