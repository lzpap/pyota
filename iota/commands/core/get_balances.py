# coding=utf-8
from __future__ import absolute_import, division, print_function, \
    unicode_literals

import filters as f
from six import iteritems

from iota import TransactionHash
from iota.commands import FilterCommand, RequestFilter, ResponseFilter
from iota.filters import AddressNoChecksum, StringifiedTrytesArray, Trytes

__all__ = [
    'GetBalancesCommand',
]


class GetBalancesCommand(FilterCommand):
    """
    Executes `getBalances` command.

    See :py:meth:`iota.api.StrictIota.get_balances`.
    """
    command = 'getBalances'

    def get_request_filter(self):
        return GetBalancesRequestFilter()

    def get_response_filter(self):
        return GetBalancesResponseFilter()


class GetBalancesRequestFilter(RequestFilter):
    def __init__(self):
        super(GetBalancesRequestFilter, self).__init__(
            {
                'addresses':
                    f.Required | f.Array | f.FilterRepeater(
                        f.Required |
                        AddressNoChecksum() |
                        f.Unicode(encoding='ascii', normalize=False),
                    ),

                'threshold':
                    f.Type(int) |
                    f.Min(0) |
                    f.Max(100) |
                    f.Optional(default=100),

                'tips': StringifiedTrytesArray(TransactionHash),
            },

            allow_missing_keys={
                'threshold', 'tips',
            },
        )

    def _apply(self, value):
        value = super(GetBalancesRequestFilter, self)._apply(
            value
        )  # type: dict

        if self._has_errors:
            return value

        # Remove null search terms.
        # Note: We will assume that empty lists are intentional.
        search_terms = {
            term: query
            for term, query in iteritems(value)
            if query is not None
        }

        return search_terms


class GetBalancesResponseFilter(ResponseFilter):
    def __init__(self):
        super(GetBalancesResponseFilter, self).__init__({
            'balances': f.Array | f.FilterRepeater(f.Int),

            'references':
                f.Array | f.FilterRepeater(
                    f.ByteString(encoding='ascii') |
                    Trytes(TransactionHash)
                ),
        })
