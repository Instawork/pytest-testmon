package sk.infinit.testmon.toolWindow

import com.intellij.openapi.module.ModuleManager
import com.intellij.openapi.project.Project
import com.intellij.openapi.wm.ToolWindow
import com.intellij.openapi.wm.ToolWindowFactory
import sk.infinit.testmon.getModuleRuntimeInfoFiles

/**
 * Factory for runtime info [ToolWindow].
 */
class RuntimeInfoToolWindowFactory : ToolWindowFactory {

    /**
     * Create list with registered (exists) runtime-info files.
     */
    override fun createToolWindowContent(project: Project, toolWindow: ToolWindow) {
        val runtimeInfoListPanel = RuntimeInfoListPanel()

        for (module in ModuleManager.getInstance(project).modules) {
            val moduleRuntimeInfoFiles = getModuleRuntimeInfoFiles(module)

            if (moduleRuntimeInfoFiles != null) {
                for (moduleRuntimeInfoFile in moduleRuntimeInfoFiles) {
                    runtimeInfoListPanel.listModel.addElement(moduleRuntimeInfoFile)
                }
            }
        }

        val contentManager = toolWindow.contentManager

        val content = contentManager.factory.createContent(runtimeInfoListPanel, null, false)

        contentManager.addContent(content)
    }
}