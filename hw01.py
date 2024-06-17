from logging import basicConfig, error, INFO, info
from pathlib import Path
from sys import argv


def main() -> None:
    basicConfig(format='%(levelname)s: %(message)s', level=INFO)

    if len(argv) < 2:
        error('Specify source folder as first argument of script.')
    else:
        path = Path(source := argv[1])

        if path.exists():
            if path.is_dir():
                target = argv[2] if len(argv) > 2 else 'dist'
                info(f'Copy files from folder "{path.absolute().name}" to '
                     f'"{target}".')
            else:
                error(f'The source "{source}" is not folder.')
        else:
            error(f'The source folder "{source}" not found.')


if __name__ == '__main__':
    main()
