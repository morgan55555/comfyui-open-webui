import { app } from "/scripts/app.js";

app.registerExtension({
    name: "Comfy.OpenwebuiNode",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (["OpenwebuiGenerate", "OpenwebuiVision"].includes(nodeData.name) ) {
      const originalNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        if (originalNodeCreated) {
          originalNodeCreated.apply(this, arguments);
        }

        const modelWidget = this.widgets.find((w) => w.name === "model");

        const fetchModels = async () => {
          try {
            const response = await fetch("/openwebui/get_models", {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
              },
            });

            if (response.ok) {
              const models = await response.json();
              console.debug("Fetched models:", models);
              return models;
            } else {
              console.error(`Failed to fetch models: ${response.status}`);
              return [];
            }
          } catch (error) {
            console.error(`Error fetching models`, error);
            return [];
          }
        };

        const updateModels = async () => {
          const prevValue = modelWidget.value
          modelWidget.value = ''
          modelWidget.options.values = []

          const models = await fetchModels();

          // Update modelWidget options and value
          modelWidget.options.values = models;
          console.debug("Updated modelWidget.options.values:", modelWidget.options.values);

          if (models.includes(prevValue)) {
            modelWidget.value = prevValue; // stay on current.
          } else if (models.length > 0) {
            modelWidget.value = models[0]; // set first as default.
          }

          console.debug("Updated modelWidget.value:", modelWidget.value);
        };



        const dummy = async () => {
          // calling async method will update the widgets with actual value from the browser and not the default from Node definition.
        }

        // Initial update
        await dummy(); // this will cause the widgets to obtain the actual value from web page.
        await updateModels();
      };
    }
  },
});
