FROM ollama/ollama:0.30.0-rc25-rocm


# RUN ollama pull gemma4:e2b
RUN (ollama serve &) \
    && sleep 5 \
    && ollama pull gemma4:31b-cloud \
    && pkill ollama