from logging import DEBUG, basicConfig, debug, error, info
from pathlib import Path
from shutil import copy
from sys import argv


def scan(source: Path, target: Path) -> None:
    for item in source.iterdir():
        if item.is_dir():
            scan(item, target)
        else:
            sub_target = target / item.suffix[1:] / item.name

            if sub_target.exists():
                debug(f'Skip file "{item.absolute()}".')
            else:
                debug(f'Copying file "{item.absolute()}" to folder '
                      f'"{sub_target.absolute()}"...')

                sub_target.mkdir(parents=True, exist_ok=True)
                copy(item, sub_target)


def main() -> None:
    basicConfig(format='%(levelname)s: %(message)s', level=DEBUG)

    if len(argv) < 2:
        error('Specify the source folder as the first argument of the script.')
    else:
        source = Path(argv[1])

        if source.exists():
            if source.is_dir():
                target = Path(argv[2] if len(argv) > 2 else 'dist')

                if target.exists() and not target.is_dir():
                    error(f'The target "{target}" is not a folder.')
                else:
                    info(f'Copying files from folder "{source.absolute()}" to '
                         f'"{target.absolute()}"...')

                    scan(source, target)
            else:
                error(f'The source "{source}" is not a folder.')
        else:
            error(f'The source folder "{source}" not found.')


if __name__ == '__main__':
    main()
