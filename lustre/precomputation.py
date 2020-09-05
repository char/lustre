import typing
import importlib, importlib.resources

from markupsafe import Markup


class Precomputation:  # TODO: Can we think of a better name for this?
    def __init__(self, precomputation_package: str):
        self.precomputation_package = precomputation_package
        self.cache = {}

    def text_file(self, path: str) -> typing.TextIO:
        directories, slash, resource = path.rpartition("/")

        package = self.precomputation_package
        if slash:
            package += "." + ".".join(directories.split("/"))

        return importlib.resources.open_text(package, resource)

    def __call__(self, *args, **kwargs) -> Markup:
        return Markup(self.get(*args, **kwargs))

    def _generate_identifier(self, name: str, *args, **kwargs):
        yield name
        yield "("

        if args:
            yield repr(args)[1:-2]

        if args and kwargs:
            yield ", "

        if kwargs:
            yield "**"
            yield repr(kwargs)

        yield ")"

    def get(self, processor: str, *args, **kwargs) -> typing.Any:
        identifier = "".join(self._generate_identifier(processor, *args, **kwargs))
        if identifier in self.cache:
            return self.cache.get(identifier)

        try:
            result = importlib.import_module(
                f"{self.precomputation_package}.{processor}"
            ).process(self, *args, **kwargs)
            self.cache[identifier] = result
            return result
        except ModuleNotFoundError:
            return None
