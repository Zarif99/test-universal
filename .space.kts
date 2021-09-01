import java.io.*
import space.jetbrains.api.runtime.helpers.message
import space.jetbrains.api.runtime.types.*


job("Flake 8") {
    startOn {
        gitPush {
            branchFilter {
                +"refs/heads/main"
                +"refs/heads/dev"
                +Regex("feature")
            }
        }
    }

    container(displayName = "Lint", image = "docsie.registry.jetbrains.space/p/doc/docsie/docsie-flake8:latest") {
        shellScript {
            content = """
                    flake8 --output-file=$mountDir/share/flake8.txt --exit-zero docsie_universal_importer/
                """
        }
    }
    
    container(displayName = "Create issues", image = "openjdk:11") {
    	kotlinScript { api ->
            api.fileShare().locate("flake8.txt")?.let {
                val recipient = MessageRecipient.Channel(ChatChannel.FromName("UniversalDocImporter Flake8"))
                val content = ChatMessage.Text("`${api.gitBranch()} pushed. Run #${api.executionNumber()}`")
                api.space().chats.messages.sendMessage(recipient, content)

                it.readText().lines().forEach { line ->
                    try {
                        val matchResult = Regex("""(.+):(\d):(\d):(.+)""").find(line)
                        val (filename, row, col, text) = matchResult!!.destructured

                        val recipient = MessageRecipient.Channel(ChatChannel.FromName("UniversalDocImporter Flake8"))
                        val content = Message(filename, row, col, text)
                        api.space().chats.messages.sendMessage(recipient, content)
                    } catch (e: Exception) {
                        println(line)
                        println(e)
                    }
                }
            }
        }   
    }
}

fun Message(filename: String, row: String, col: String, text: String): ChatMessage {
    return message {
        outline = MessageOutline(
            icon = ApiIcon("smile"),
            text = "Flake8 error"
        )
        section {
            header = text
            fields {
                field("Filename", "`$filename`")
                field("Row", row)
                field("Col", col)
            }
        }
    }

}