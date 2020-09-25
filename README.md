

# AWS WAF OPERATIONS

#### Construa dashboards operacionais no Elasticsearch para operação do AWS WAF

Neste repositório, compartilhamos código python para adaptação dos logs do AWS WAF (usando o lambda de transformação do Kinesis Firehose) e templates de dashboards para o Kibana.

![img](assets/SETUP/dashboard1.png)



A implementação está baseada neste blogpost, atualizando a versão do ES para 7:
https://aws.amazon.com/pt/blogs/security/how-to-analyze-aws-waf-logs-using-amazon-elasticsearch-service/



### Instalação

Para fazer a instalação, precisamos criar um bucket no S3 e salvar os arquivos .ZIP contendo as funções Lambda. Clone o repositório (com o comando `git clone git@github.com:danidoo/aws-waf-operations.git`) ou efetue o download dos arquivos `waf_operations.yaml, lambda.zip e cr_lambda.zip` . Crie um bucket S3 na conta onde o deploy da solução será executado, crie uma pasta para organizar os arquivos e faça o upload:

![image-20200925154843355](assets/SETUP/image-20200925154843355.png)



![image-20200925154937313](assets/SETUP/image-20200925154937313.png)



![image-20200925155055974](assets/SETUP/image-20200925155055974.png)



Depois de fazer o upload dos arquivos, abra a console do CloudFormation, clique em Create Stack e coloque a URL do arquivo yaml que acabamos de salvar no S3:

![image-20200925155538671](assets/SETUP/image-20200925155538671.png)



Na próxima tela, defina um nome para a stack e preencha os parâmetros obrigatórios (Bucket, BucketKey e E-mail):

![image-20200925155808637](assets/SETUP/image-20200925155808637.png)



Na última tela, autorize o CloudFormation a criar recursos do IAM:

![image-20200925155942244](assets/SETUP/image-20200925155942244.png)



O próximo passo deve demorar de 30 a 40 minutos:

![image-20200925160053981](assets/SETUP/image-20200925160053981.png)



Durante o processo, você deve receber um e-mail com credenciais temporárias:

![image-20200925161727428](assets/SETUP/image-20200925161727428.png)



Quando o processo de deploy for concluído, podemos acessar o dashboard do Kibana através da URL do ElasticSearch + o sulfixo /_plugin/kibana. A URL do ES pode ser encontrada na aba Outputs:

![image-20200925162643090](assets/SETUP/image-20200925162643090.png)



A tela do Cognito será exibida. Utilize as credenciais enviadas no e-maill:

![image-20200925162803971](assets/SETUP/image-20200925162803971.png)



![image-20200925162914631](assets/SETUP/image-20200925162914631.png)



![image-20200925162945946](assets/SETUP/image-20200925162945946.png)



Ao abrir os dashboards, você perceberá que eles estão sem dados. Para começar a contagem, acesse o WAF, ative os logs e direcione a saída para o Kinesis Firehose. Assim que os requests chegarem, as métricas começarão a ser preenchidas:

![image-20200925163113523](assets/SETUP/image-20200925163113523.png)



![image-20200925163144924](assets/SETUP/image-20200925163144924.png)



E este é o Dashboard com dados:

![img](assets/SETUP/dashboard1.png)





### Desinstalação

Para remover a solução, basta deletar a stack via CloudFormation.