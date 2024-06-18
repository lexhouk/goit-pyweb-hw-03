from abc import ABC, abstractmethod
from logging import INFO, basicConfig, error, info, warning
from pathlib import Path
from shutil import copy
from sys import argv
from threading import Semaphore, Thread


class Worker(ABC, Thread):
    _args: list[Path]

    def __init__(self,
                 source: Path,
                 target: Path,
                 semaphore: Semaphore) -> None:
        super().__init__(name=f'{self.__class__.__name__} of {source}',
                         args=(source, target))
        self._semaphore = semaphore
        self.start()

    @abstractmethod
    def _action(self) -> None:
        ...

    def run(self) -> None:
        with self._semaphore:
            self._action()


class Copyist(Worker):
    def _action(self) -> None:
        info(f'Copying the file to folder "{self._args[1]}"...')
        self._args[1].mkdir(parents=True, exist_ok=True)
        copy(*self._args)


class Scanner(Worker):
    def _action(self) -> None:
        for source in self._args[0].iterdir():
            if source.is_dir():
                Scanner(source, self._args[1], self._semaphore)
            else:
                target = self._args[1] / source.suffix[1:] / source.name

                if target.exists():
                    warning(f'Skip file "{source.name}".')
                else:
                    Copyist(source, target.parent, self._semaphore)


def main() -> None:
    basicConfig(format='%(threadName)s\n%(levelname)s: %(message)s\n',
                level=INFO)

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
                    info(f'Copying files from folder "{source}" to '
                         f'"{target}"...')

                    Scanner(source, target, Semaphore(10))
            else:
                error(f'The source "{source}" is not a folder.')
        else:
            error(f'The source folder "{source}" not found.')


if __name__ == '__main__':
    main()
