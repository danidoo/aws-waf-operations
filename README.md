# Construa dashboards operacionais no Elasticsearch para operação do AWS WAF

Neste repositório compartilho código python para adaptação dos logs do AWS WAF (usando o lambda de transformação do Kinesis Firehose) e templates de dashboards para o Kibana.

![Kibana Dashboard 1][dashboard1.png]
![Kibana Dashboard 2][dashboard2.png]



A implementação está baseada neste blogpost, atualizando a versão do ES para 7.4:
https://aws.amazon.com/pt/blogs/security/how-to-analyze-aws-waf-logs-using-amazon-elasticsearch-service/

Para a versão 7.4 do ES foi necessário adaptar o template de ingestão dos logs disponível no blogpost usando o código à seguir:

<pre>
PUT  _template/awswaf-logs
{
    "index_patterns": ["awswaf-*"],
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        "properties": {
            "httpRequest": {
                "properties": {
                    "clientIp": {
                        "type": "keyword",
                        "fields": {
                            "keyword": {
                                "type": "ip"
                            }
                        }
                    }
                }
            },
            "timestamp": {
                "type": "date",
                "format": "epoch_millis"
            }
        }
    }
}
</pre>