from django.core.management.base import BaseCommand
from backend.apps.rag_engine.client import RAGFlowClient

class Command(BaseCommand):
    help = '测试 RAGFlow 连接'

    def handle(self, *args, **options):
        self.stdout.write("正在连接 RAGFlow...")
        try:
            client = RAGFlowClient()
            self.stdout.write(f"API Base: {client.base_url}")
            
            # 1. 测试获取列表
            datasets = client.list_datasets()
            self.stdout.write(self.style.SUCCESS(f"连接成功！当前知识库数量: {len(datasets)}"))
            for ds in datasets:
                self.stdout.write(f"- [{ds['id']}] {ds['name']}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"连接失败: {str(e)}"))