"""
A Norse-style greeting module from the Well of Wisdom.

This module provides functions for generating authentic Norse greetings
worthy of the Aesir giants. Perfect for welcoming seekers of wisdom
into the Great Hall.

Example:
    >>> from mimir_forge.tools.hello_mimir import greet
    >>> greet("Odin")
    'Hail Odin, seeker of wisdom!' 

"""

from __future__ import annotations


# Traditional Norse salutations for our greetings
NORSE_SALUTATIONS: tuple[str, ...] = ("Hail", "Welcome", "Greetings")

# Honorable titles befitting those who seek wisdom
WISE_TITLES: tuple[str, ...] = (
    "seeker of wisdom",
    "keeper of knowledge",
    "student of the cosmos",
    "walker of the nine worlds",
)


def greet(name: str, title: str | None = None) -> str:
    """
    Generate a Norse-style greeting for the given name.
    
    Creates an honorable greeting worthy of the Aesir, combining
    a traditional salutation with the recipient's name and optional
    title.
    
    Args:
        name: The name of the person to greet. Should be non-empty.
        title: Optional title or epithet to append to the greeting.
               If not provided, a random title from WISE_TITLES is used.
    
    Returns:
        A formatted greeting string in the style of ancient Norse.
        
    Raises:
        ValueError: If name is empty or contains only whitespace.
        
    Example:
        >>> greet("Ymir")
        'Hail Ymir, seeker of wisdom!'
        >>> greet("Odin", "the Allfather")
        'Hail Odin, the Allfather!'
        
    """
    if not name or not name.strip():
        msg = "Name cannot be empty or whitespace only"
        raise ValueError(msg)
    
    salutation = NORSE_SALUTATIONS[0]  # Default to "Hail"
    
    if title:
        return f"{salutation} {name}, {title}!"
    
    # Select a title worthy of wisdom-seekers
    selected_title = WISE_TITLES[0]
    return f"{salutation} {name}, {selected_title}!"


def greet_all(names: list[str]) -> str:
    """
    Generate a greeting for multiple names.
    
    Creates a collective greeting for a group of wisdom-seekers,
    joining them with proper Norse conjunction.
    
    Args:
        names: A list of names to include in the greeting.
        
    Returns:
        A collective greeting string.
        
    Raises:
        ValueError: If names list is empty.
        
    Example:
        >>> greet_all(["Odin", "Thor", "Loki"])
        'Hail Odin, Thor, and Loki, seekers of wisdom!'
        
    """
    if not names:
        msg = "Cannot greet an empty assembly"
        raise ValueError(msg)
    
    if len(names) == 1:
        return greet(names[0])
    
    # Norse style: "A, B, and C"
    joined = ", ".join(names[:-1]) + ", and " + names[-1]
    title = "seeker of wisdom" if len(names) == 2 else "seekers of wisdom"
    return f"Hail {joined}, {title}!"


# Allow the module to be run directly for testing
if __name__ == "__main__":
    # Demonstrate the greeting functions
    print("=" * 50)
    print("  From the Well of Wisdom...")
    print("=" * 50)
    print()
    
    # Single greeting
    print(greet("Ymir"))
    print(greet("Odin", "the Allfather"))
    print()
    
    # Group greeting
    print(greet_all(["Odin", "Thor", "Loki"]))
    print()
    
    print("May wisdom guide your path.")
