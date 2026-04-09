FROM ollama/ollama:0.12.9

# RUN ollama pull gemma4:e2b
RUN (ollama serve &) \
    && sleep 5 \
    && ollama pull gemma4:e2b \
    && pkill ollama
