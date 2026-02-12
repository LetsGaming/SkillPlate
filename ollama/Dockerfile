FROM ollama/ollama:0.12.9

# RUN ollama pull gemma3:270m
RUN (ollama serve &) \
    && sleep 5 \
    && ollama pull gemma3:270m \
    && pkill ollama
