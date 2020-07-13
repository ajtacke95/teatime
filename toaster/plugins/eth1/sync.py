"""This module contains a plugin checking for node sync issues."""

import requests

from toaster.plugins import Context, NodeType, Plugin
from toaster.reporting import Issue, Severity


class NodeSyncedCheck(Plugin):
    """A plugin to check for issues in node synchronization."""
    name = "RPC Node Sync Status"
    version = "0.2.0"
    node_type = (NodeType.GETH, NodeType.PARITY)

    def __repr__(self):
        return f"<NodeSyncedCheck v{self.version}>"

    def check_sync(self, context):
        """Check the node's sync state and whether it's stuck.

        .. todo:: Add details!

        :param context:
        """
        node_syncing = self.get_rpc_json(context.target, "eth_syncing")
        node_blocknum = int(self.get_rpc_json(context.target, "eth_blockNumber"), 16)
        net_blocknum = self.get_latest_block_number()
        block_threshold = 10

        if node_blocknum < (net_blocknum - block_threshold) and not node_syncing:
            context.report.add_issue(
                Issue(
                    title="Synchronization Status",
                    description="The node's block number is stale and its not synchronizing. The node is stuck!",
                    raw_data=node_syncing,
                    severity=Severity.CRITICAL,
                )
            )
        else:
            # TODO: More info if node is syncing? E.g. how many blocks to go
            context.report.add_issue(
                Issue(
                    title="Synchronization Status",
                    description=f"Syncing: {node_syncing} Block Number: {node_blocknum}",
                    raw_data=node_syncing,
                    severity=Severity.NONE,
                )
            )

    @staticmethod
    def get_latest_block_number() -> int:
        """Fetch the latest block number.

        .. todo:: Add details!

        :return:
        """
        rpc_response = requests.post(
            "https://mainnet.infura.io/v3/a17bd235fd4147259d03784b24bd3a62",
            json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
        )
        # TODO: Better error handling
        return int(rpc_response.json()["result"], 16)

    def run(self, context: Context):
        """Run the node sync check plugin.

        .. todo:: Add details!

        :param context:
        """
        # SCAN[CRITICAL]: Node sync stuck at old block
        # SCAN[NONE]: Node is still syncing
        self.run_catch("Sync status", self.check_sync, context)
        context.report.add_meta(self.name, self.version)