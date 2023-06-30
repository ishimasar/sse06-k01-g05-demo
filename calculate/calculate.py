import json
from pathlib import Path


def add_text(bread_data: dict):
    if bread_data['reservation']:
        text = '予約承り中'
    elif bread_data['stock'] < 1:
        text = '完売しました'
    elif bread_data['stock'] < 5:
        text = f'△あと{bread_data["stock"]}個'
    else:
        text = '在庫あり'
    bread_data['text'] = text
    return bread_data


def read_json(path: Path):
    with path.open() as f:
        data = json.load(f)
    return data


if __name__ == '__main__':
    inventory = read_json(Path('bread_inventory.json'))
    output_text = [add_text(i) for i in inventory]

    for output in output_text:
        print('bread_name: ', output['bread_name'])
        print('price: ', output['price'])
        print('stock: ', output['stock'])
        print('reservation: ', output['reservation'])
        print('text: ', output['text'])
        print()
