import json

from loguru import logger
def extract_product_info(data) -> str:
    if 'product' in data:
        data = data['product']
    if type(data) == str:
        data = json.loads(data)
    cells = []
    for header, cell in data.items():
        cell=str(cell)
        cell=cell.replace(',', '').replace(',','')
        cells.append(cell)

    row_write = ','.join(cells)
    # logger.info(row_write)
    return row_write

# https://www.amazon.co.jp/KAIKEA-1-%E3%83%A9%E3%82%A4%E3%83%88%E3%83%9A%E3%83%B3%E3%83%80%E3%83%B3%E3%83%88%E7%85%A7%E6%98%8E%E5%99%A8%E5%85%B7%E5%B1%8B%E5%A4%96%E3%83%9A%E3%83%B3%E3%83%80%E3%83%B3%E3%83%88%E3%83%A9%E3%83%B3%E3%83%978-3-%E3%80%81%E3%83%9D%E3%83%BC%E3%83%81%E3%83%B4%E3%82%A3%E3%83%A9%E9%80%9A%E8%B7%AF%E3%83%90%E3%83%AB%E3%82%B3%E3%83%8B%E3%83%BC%E3%82%AC%E3%83%AC%E3%83%BC%E3%82%B8%E7%94%A8%E3%81%AE%E7%B4%A0%E6%9C%B4%E3%81%AA%E5%B1%8B%E5%A4%96%E3%83%9A%E3%83%B3%E3%83%80%E3%83%B3%E3%83%88%E3%83%A9%E3%83%B3%E3%82%BF%E3%83%B3%E3%81%AE%E8%BE%B2%E5%AE%B6%E3%81%AE%E5%A4%96%E9%83%A8%E5%90%8A%E3%82%8A%E4%B8%8B%E3%81%92%E3%83%A9%E3%82%A4%E3%83%88/dp/B09KG7S4RP/ref=sr_1_29?m=A11BFGJBAHXX7B&marketplaceID=A1VC38T7YXB528&qid=1694687204&s=merchant-items&sr=1-29&th=1

