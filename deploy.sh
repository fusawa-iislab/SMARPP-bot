#!/bin/bash

set -e  # エラーで止める

# 環境変数
export PROJECT_ID=yugo-master-thesis
export SERVICE_NAME=smarpp-bot-proto
export IMAGE_NAME=gcr.io/$PROJECT_ID/$SERVICE_NAME
export REGION=asia-northeast1

# .env ファイルが存在するか確認
if [ ! -f .env ]; then
  echo ".env ファイルが見つかりません"
  exit 1
fi

# env.yaml を作成
echo "🔧 .env から env.yaml を生成中..."
echo "" > env.yaml
grep -v '^#' .env | grep -v '^\s*$' | while IFS='=' read -r key value; do
  key=$(echo $key | xargs)  # key の前後空白除去
  value=$(echo $value | xargs)  # value の前後空白除去
  echo "$key: \"$value\"" >> env.yaml
done

# GCP 設定
echo "✅ プロジェクトを設定: $PROJECT_ID"
gcloud config set project $PROJECT_ID
gcloud services enable run.googleapis.com

# Docker イメージをビルド & アップロード
echo "🐳 Docker イメージをビルド中..."
gcloud builds submit --tag $IMAGE_NAME .

# Cloud Run にデプロイ
echo "🚀 Cloud Run にデプロイ中..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --env-vars-file env.yaml

# env.yaml を削除
echo "🧹 env.yaml を削除中..."
rm env.yaml

echo "✅ デプロイ完了！"