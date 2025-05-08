// NSwapInputNodeS.js
import { app } from "../../../scripts/app.js";
import { api } from "../../../scripts/api.js";

app.registerExtension({
    name: "Comfy.NSwapInput",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "N_SwapInput") return;

        const origOnNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function() {
            const result = origOnNodeCreated?.apply(this, arguments);

            const backupBtn = this.addWidget("button", "backup_input", "Backup Input 💾",
                async () => {
                    try {
                        const backup_suffix = this.widgets.find(w => w.name === "backup_suffix")?.value;
                        if (!backup_suffix) {
                            alert("Please select a folder suffix");
                            return;
                        }
                        const options = {
                            backup_suffix: backup_suffix,
                        };
                        const response = await api.fetchApi("/N_swapinput/backup_input", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(options)
                        });

                        if (!response.ok) throw new Error(await response.text());
                        const result = await response.json();

                        if (!result.success) {
                            throw new Error(result.error);
                        }

                        alert("Input folder backed up successfully");
                    } catch (error) {
                        console.error("Backup error:", error);
                        alert(error.message);
                    }
                }
            );

            const restoreBtn = this.addWidget("button", "restore_input", "Restore Input ♻️",
                async () => {
                    try {
                         const backup_suffix = this.widgets.find(w => w.name === "backup_suffix")?.value;
                        if (!backup_suffix) {
                            alert("Please select a folder suffix");
                            return;
                        }
                        const options = {
                            backup_suffix: backup_suffix,
                        };
                        const response = await api.fetchApi("/N_swapinput/restore_input", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify(options)
                        });

                        if (!response.ok) throw new Error(await response.text());
                        const result = await response.json();

                        if (!result.success) {
                            throw new Error(result.error);
                        }

                        alert("Input folder restored successfully");

                        // Refresh previews after restore
                        const refreshBtn = this.widgets.find(w => w.name === "refresh_preview");
                        if (refreshBtn?.callback) {
                            setTimeout(() => refreshBtn.callback(), 100);
                        }
                    } catch (error) {
                        console.error("Restore error:", error);
                        alert(error.message);
                    }
                }
            );

            return result;
        };





    }
});
