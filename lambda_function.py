# coding:utf-8
import boto3

def lambda_handler(event, context):
    # コミットID取得 eventから関数起動元であるCodeCommitの情報を取得可能
    commit_id = event['Records'][0]['codecommit']['references'][0]['commit']
    # レポジトリ名を取得
    rep = event['Records'][0]['eventSourceARN'].split(":")[5]
    
    s3 = boto3.client('s3')
    codecommit = boto3.client('codecommit')
    
    # コミット内ファイル情報の取得
    files = codecommit.get_differences(repositoryName=rep,afterCommitSpecifier=commit_id)['differences']
    
    # ファイルごとの操作
    for file in files:
        # パス整形
        path = rep + '/' + file['afterBlob']['path']
        # BlobIdの取得
        blobid = file['afterBlob']['blobId']
        # ファイル内の情報を取得
        content = codecommit.get_blob(repositoryName=rep,blobId=blobid)['content']
        # 特定のS3バケットへ保存 レポジトリごとにフォルダを分けて保存できる
        s3.put_object(Bucket='バケット名',Key=path,Body=content)