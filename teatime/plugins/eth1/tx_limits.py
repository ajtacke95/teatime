"""This module contains plugins around setting transaction-related limits."""
from teatime.plugins import Context, NodeType, Plugin
from teatime.reporting import Issue, Severity


class ParityTxCeiling(Plugin):
    """Try to set the maximum transaction gas.

    Severity: Critical

    Parity/OpenEthereum: https://openethereum.github.io/wiki/JSONRPC-parity_set-module#parity_setmaxtransactiongas
    """

    INTRUSIVE = True

    def __init__(self, gas_limit: str):
        self.gas_limit = gas_limit

    def _check(self, context: Context) -> None:
        if context.node_type != NodeType.PARITY:
            return

        payload = self.get_rpc_json(
            context.target,
            method="parity_setMaxTransactionGas",
            params=[self.gas_limit],
        )
        context.report.add_issue(
            Issue(
                title="Transaction maximum gas can be changed",
                description="Anyone can change the maximum transaction gas limit using the "
                "parity_setMaxTransactionGas RPC call.",
                raw_data=payload,
                severity=Severity.CRITICAL,
            )
        )


class ParityMinGasPrice(Plugin):
    """Try to set the minimum transaction gas price.

    Severity: Critical

    Parity/OpenEthereum: https://openethereum.github.io/wiki/JSONRPC-parity_set-module#parity_setmingasprice
    """

    INTRUSIVE = True

    def __init__(self, gas_price: str):
        self.gas_price = gas_price

    def _check(self, context: Context) -> None:
        if context.node_type != NodeType.PARITY:
            return

        payload = self.get_rpc_json(
            context.target, method="parity_setMinGasPrice", params=[self.gas_price]
        )
        context.report.add_issue(
            Issue(
                title="Transaction minimum gas can be changed",
                description="Anyone can change the minimum transaction gas limit using the parity_setMinGasPrice RPC "
                "call.",
                raw_data=payload,
                severity=Severity.CRITICAL,
            )
        )
