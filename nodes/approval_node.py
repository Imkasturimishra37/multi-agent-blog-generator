from state.blog_state import BlogState


def approval_node(state: BlogState):

    print("\n========== GENERATED OUTLINE ==========\n")
    print(state["outline"])

    choice = input("\nApprove this outline? (yes/no): ").lower()

    if choice == "yes":
        return {
            "approved": True,
            "feedback": ""
        }

    feedback = input(
        "\nWhy are you rejecting it? Give feedback: "
    )

    return {
        "approved": False,
        "feedback": feedback
    }
