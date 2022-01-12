import commands.handler as handler
from spreadsheet import ss
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from utils import subsystems


def bt(update: Update, ctx: CallbackContext) -> None:
    handler.log_command("baterias")
    subsystem_generic(update, ctx, "bt")

def pt(update: Update, ctx: CallbackContext) -> None:
    handler.log_command("powertrain")
    subsystem_generic(update, ctx, "pt")

def hw(update: Update, ctx: CallbackContext) -> None:
    handler.log_command("hardware")
    subsystem_generic(update, ctx, "hw")

def sw(update: Update, ctx: CallbackContext) -> None:
    handler.log_command("software")
    subsystem_generic(update, ctx, "sw")



def get_task_lister_text(subsystem: str) -> str:
    todo_tasks = "\n".join([f"{index+1} - {row[0]}" 
                            for index, row in enumerate(
                                row for row in ss.sheet(subsystem).get_all_values()
                                if row[1] in ["Fazendo", "A fazer"] and row[0])])
    
    return (f"<b>Subsistema: {subsystems[subsystem]['name']}</b>\n\n"
                "<u>Tarefas:</u>\n"
                f"{todo_tasks}\n\n"
                f"Para concluir uma tarefa, utilize <code>/{subsystem} c &lt;número | nome da tarefa&gt;</code>"
                ).format(todo_tasks=todo_tasks)


def subsystem_task_lister(update: Update, ctx: CallbackContext, sub: str, args: str) -> None:
    if not args:
        update.message.reply_text(get_task_lister_text(sub), parse_mode=ParseMode.HTML)

    else:
        print(f"Conclude task {args}")


def get_default_text(sub: str) -> str:
    return (
            f"<b>Subsistema: {subsystems[sub]['name']}</b>\n"
            f"<u>Tarefas:</u> {len(ss.sheet(sub).get_all_values())}\n\n"
            "<u>Funções</u>\n"
            "<code>l</code> - Listar tarefas\n"
            "<code>i</code> - Iniciar tarefa\n"
            "<code>c</code> - Concluir tarefa\n"
            "<code>a</code> - Adicionar tarefa\n"
            "<code>u</code> - Atualizar tarefa"
        )


def subsystem_generic(update: Update, ctx: CallbackContext, sub: str) -> None:
    if not ctx.args:
        update.message.reply_text(get_default_text(sub), parse_mode=ParseMode.HTML)

    else:
        function = ctx.args[0]
        args = " ".join(ctx.args[1:])

        if function not in ["l", "i", "c", "a", "u"]:
            update.message.reply_text(get_default_text(sub), parse_mode=ParseMode.HTML)

        elif function == "l":
            subsystem_task_lister(update, ctx, sub, args)

        elif function == "i":
            print("insert task")
        
        elif function == "c":
            print("conclude task")

        elif function == "a":
            print("add task")

        elif function == "u":
            print("update task")
        
        



    