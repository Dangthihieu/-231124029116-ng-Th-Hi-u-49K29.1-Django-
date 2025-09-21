# import csv
# from django.core.management.base import BaseCommand
# from data_sheet.models import Customer, ProductGroup, Product, Order, OrderDetail
# from datetime import datetime
# import os

# class Command(BaseCommand):
#     help = 'Import dữ liệu từ data_sheet.csv vào database'

#     def handle(self, *args, **kwargs):
#         # Lấy đường dẫn tuyệt đối tới file CSV (đặt cạnh manage.py)
#         base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#         csv_file = os.path.join(base_dir, "data_sheet.csv")

#         with open(csv_file, newline='', encoding='utf-8') as f:
#             reader = csv.DictReader(f)
#             for row in reader:
#                 # Customer
#                 customer, _ = Customer.objects.get_or_create(
#                     customer_id=row['customer_id'],
#                     defaults={
#                         'name': row['customer_name'],
#                         'segment_code': row['segment_code']
#                     }
#                 )

#                 # ProductGroup
#                 product_group, _ = ProductGroup.objects.get_or_create(
#                     group_code=row['group_code']
#                 )

#                 # Product
#                 product, _ = Product.objects.get_or_create(
#                     product_code=row['product_code'],
#                     defaults={
#                         'name': row['product_name'],
#                         'group': product_group,
#                         'unit_price': int(row['unit_price'])
#                     }
#                 )

#                 # Order
#                 order_time = datetime.strptime(row['order_time'], "%Y-%m-%d %H:%M:%S")
#                 order, _ = Order.objects.get_or_create(
#                     order_id=row['order_id'],
#                     defaults={'customer': customer, 'order_time': order_time}
#                 )

#                 # OrderDetail
#                 OrderDetail.objects.get_or_create(
#                     order=order,
#                     product=product,
#                     defaults={'quantity': int(row['quantity'])}
#                 )

#         self.stdout.write(self.style.SUCCESS("✅ Import dữ liệu từ data_sheet.csv thành công!"))
import csv
from django.core.management.base import BaseCommand
from data_sheet.models import Customer, ProductGroup, Product, Order, OrderDetail
from django.utils import timezone
import datetime
import os

class Command(BaseCommand):
    help = 'Import dữ liệu từ CSV vào database'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help=r'D:\TRƯỜNG ĐẠI HỌC KINH TẾ\Năm 3 kỳ 1( 2025-2026)\Trực quan hóa dữ liệu\Django\Tuan8_Django\data_ggsheet.csv'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['file_path']

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f"File không tồn tại: {csv_file}"))
            return

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Customer
                customer, _ = Customer.objects.get_or_create(
                    customer_id=row['Mã khách hàng'],
                    defaults={
                        'name': row['Tên khách hàng'],
                        'segment_code': row['Mô tả Phân Khúc Khách hàng']
                    }
                )

                # ProductGroup
                product_group, _ = ProductGroup.objects.get_or_create(
                    group_code=row['Mã nhóm hàng']
                )

                # Product
                product, _ = Product.objects.get_or_create(
                    product_code=row['Mã mặt hàng'],
                    defaults={
                        'name': row['Tên mặt hàng'],
                        'group': product_group,
                        'unit_price': int(row['Đơn giá'])
                    }
                )

                # Order
                order_time = datetime.datetime.strptime(row['Thời gian tạo đơn'], "%Y-%m-%d %H:%M:%S")
                order_time = timezone.make_aware(order_time, timezone.get_current_timezone())
                order, _ = Order.objects.get_or_create(
                    order_id=row['Mã đơn hàng'],
                    defaults={'customer': customer, 'order_time': order_time}
                )

                # OrderDetail
                OrderDetail.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={'quantity': int(row['SL'])}
                )

        self.stdout.write(self.style.SUCCESS(f"✅ Import dữ liệu từ {csv_file} thành công!"))
