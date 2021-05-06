import pytest

from typing import (
    Any,
)

from prototypes import (
    prototype,
    PrototypeError,
)


def test_prototype_does_not_modify_function() -> None:
    def proto() -> None:
        pass

    def func() -> None:
        pass

    assert prototype(proto)(func) is func


def test_prototype_with_no_runtime_does_not_modify_function() -> None:
    def proto() -> None:
        pass

    def func() -> None:
        pass

    assert prototype(proto, runtime=False)(func) is func


def test_prototype_with_no_runtime_does_raise_error_during_runtime() -> None:
    def proto() -> None:
        pass

    # noinspection PyUnusedLocal
    @prototype(proto, runtime=False)
    def func(x: int, /) -> None:
        pass


def test_prototype_error_on_no_parameters_annotation() -> None:
    # noinspection PyUnusedLocal
    def proto(x: int) -> None:
        pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func(x):  # type: ignore
            pass


def test_prototype_error_on_func_positional_only_parameters() -> None:
    # noinspection PyUnusedLocal
    def proto(x: int) -> None:
        pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func(x: int, /) -> None:
            pass


def test_prototype_error_on_proto_positional_only_parameters() -> None:
    # noinspection PyUnusedLocal
    def proto(x: int, /) -> None:
        pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func(x: int) -> None:
            pass


def test_prototype_error_on_func_keyword_only_parameters() -> None:
    # noinspection PyUnusedLocal
    def proto(x: int) -> None:
        pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func(*, x: int) -> None:
            pass


def test_prototype_error_on_proto_keyword_only_parameters() -> None:
    # noinspection PyUnusedLocal
    def proto(*, x: int) -> None:
        pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func(x: int) -> None:
            pass


def test_prototype_error_on_args_kwargs() -> None:
    # noinspection PyUnusedLocal
    def proto(*args: Any, **kwargs: Any) -> None:
        pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func_with_only_args(*args: Any) -> None:
            pass

    with pytest.raises(PrototypeError):
        # noinspection PyUnusedLocal
        @prototype(proto)
        def func_with_only_kwargs(**kwargs: Any) -> None:
            pass


def test_prototype_error_on_incompatible_return_annotation() -> None:
    def proto() -> None:
        pass

    with pytest.raises(PrototypeError):

        @prototype(proto)
        def func() -> int:
            pass


def test_prototype_error_on_incompatible_return_annotation_with_inheritance() -> None:
    def proto() -> int:
        pass

    with pytest.raises(PrototypeError):

        @prototype(proto)
        def func() -> bool:
            pass


def test_prototype_error_on_no_return_annotation() -> None:
    def proto() -> None:
        pass

    with pytest.raises(PrototypeError):

        @prototype(proto)
        def func():  # type: ignore
            pass
