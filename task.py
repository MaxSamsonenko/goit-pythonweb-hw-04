import asyncio
import logging
import argparse
from aiopath import AsyncPath
from aioshutil import copyfile


logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='file_sort_errors.log',
    filemode='w'
)


async def copy_file(file_path: AsyncPath, target_dir: AsyncPath):
    ext = file_path.suffix.lower().strip('.')
    target_subdir = AsyncPath(target_dir / ext)

    if not await target_subdir.exists():
        await target_subdir.mkdir(parents=True, exist_ok=True)

    target_path = AsyncPath(target_subdir / file_path.name)

    try:
        await copyfile(file_path, target_path)
        print(f"Копійовано: {file_path} → {target_path}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {file_path} -> {target_path}: {e}")

async def read_folder(source_dir: AsyncPath, target_dir: AsyncPath):
    async for path in source_dir.rglob("*"):
        if await path.is_file():
            await copy_file(path, target_dir)

async def main():
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням")
    parser.add_argument("source_dir", help="Вихідна папка")
    parser.add_argument("target_dir", help="Цільова папка")

    args = parser.parse_args()

    source_path = AsyncPath(args.source_dir)
    target_path = AsyncPath(args.target_dir)
    
    if not await source_path.exists() or not await source_path.is_dir():
        print(f"Вихідна папка '{source_path}' не існує або не є директорією.")
        return

    if not await target_path.exists():
        await target_path.mkdir(parents=True)

    await read_folder(source_path, target_path)
    
if __name__ == '__main__':
    asyncio.run(main())
