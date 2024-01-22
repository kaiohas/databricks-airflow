# Databricks notebook source
# MAGIC %pip install kaleido slack-sdk

# COMMAND ----------

import slack_sdk
from slack_sdk import WebClient

# COMMAND ----------

slack_token = "xoxb-6523760730433-6508318781637-7O0uy3IIzed01Qx4pAqYubym"
client = WebClient(token=slack_token)

# COMMAND ----------

nome_arquivo = dbutils.fs.ls("dbfs:/databricks-results/prata/valores_reais")[-1].name

# COMMAND ----------

path = "../../dbfs/databricks-results/prata/valores_reais/" + nome_arquivo

# COMMAND ----------

enviando_arquivo_csv = client.files_upload_v2(
    channel = "C06F13VFA58",
    title = "Arquivo no formato CSV do valor do real convertido",
    file = path,
    filename="Valores_reais.csv",
    initial_comment="Segue anexo o arquivo CSV:",
)

# COMMAND ----------


