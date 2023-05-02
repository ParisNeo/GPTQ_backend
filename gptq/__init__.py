######
# Project       : GPT4ALL-UI
# File          : backend.py
# Author        : ParisNeo with the help of the community
# Supported by Nomic-AI
# Licence       : Apache 2.0
# Description   : 
# This is an interface class for GPT4All-ui backends.
######
from pathlib import Path
from typing import Callable
from transformers import AutoTokenizer, TextGenerationPipeline
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
from pyGpt4All.backend import GPTBackend
import torch

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/GPTQ_backend"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"

backend_name = "GPTQ"

class GPTQ(GPTBackend):
    file_extension='*.bin'
    def __init__(self, config:dict) -> None:
        """Builds a GPTQ backend

        Args:
            config (dict): The configuration file
        """
        super().__init__(config, False)
        
        self.model_dir = f'models/gptq/{config["model"]}'


        self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir, use_fast=True)

        # load quantized model, currently only support cpu or single gpu
        self.model = AutoGPTQForCausalLM.from_quantized(self.model_dir, device="cuda:0", use_triton=False)


    def stop_generation(self):
        self.model._grab_text_callback()

    def generate(self, 
                 prompt:str,                  
                 n_predict: int = 128,
                 new_text_callback: Callable[[str], None] = bool,
                 verbose: bool = False,
                 **gpt_params ):
        """Generates text out of a prompt

        Args:
            prompt (str): The prompt to use for generation
            n_predict (int, optional): Number of tokens to prodict. Defaults to 128.
            new_text_callback (Callable[[str], None], optional): A callback function that is called everytime a new text element is generated. Defaults to None.
            verbose (bool, optional): If true, the code will spit many informations about the generation process. Defaults to False.
        """
        try:
            tok = self.tokenizer.decode(self.model.generate(**self.tokenizer(prompt, return_tensors="pt").to("cuda:0"))[0])
            new_text_callback(tok)
            """
            self.model.reset()
            for tok in self.model.generate(prompt, 
                                           n_predict=n_predict,                                           
                                            temp=self.config['temp'],
                                            top_k=self.config['top_k'],
                                            top_p=self.config['top_p'],
                                            repeat_penalty=self.config['repeat_penalty'],
                                            repeat_last_n = self.config['repeat_last_n'],
                                            n_threads=self.config['n_threads'],
                                           ):
                if not new_text_callback(tok):
                    return
            """
        except Exception as ex:
            print(ex)