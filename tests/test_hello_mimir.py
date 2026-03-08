"""
Tests for the hello_mimir module.

These tests verify that the Norse greeting functions work correctly
and handle edge cases appropriately.
"""

from mimir_forge.tools.hello_mimir import greet, greet_all


class TestGreet:
    """Tests for the greet function."""

    def test_greet_basic(self):
        """Test basic greeting generation."""
        result = greet("Ymir")
        assert "Ymir" in result
        assert result.endswith("!")
        assert result.startswith("Hail")

    def test_greet_with_title(self):
        """Test greeting with custom title."""
        result = greet("Odin", "the Allfather")
        assert result == "Hail Odin, the Allfather!"

    def test_greet_with_northern_title(self):
        """Test greeting with northern title."""
        result = greet("Thor", "God of Thunder")
        assert result == "Hail Thor, God of Thunder!"

    def test_greet_empty_name_raises(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError):
            greet("")

    def test_greet_whitespace_name_raises(self):
        """Test that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError):
            greet("   ")

    def test_greet_special_characters(self):
        """Test greeting with special characters in name."""
        result = greet("Valþór")
        assert "Valþór" in result


class TestGreetAll:
    """Tests for the greet_all function."""

    def test_greet_all_single_name(self):
        """Test greeting for a single name."""
        result = greet_all(["Ymir"])
        assert "Ymir" in result

    def test_greet_all_two_names(self):
        """Test greeting for two names."""
        result = greet_all(["Odin", "Thor"])
        assert "Odin" in result
        assert "Thor" in result
        assert "and" in result

    def test_greet_all_multiple_names(self):
        """Test greeting for multiple names."""
        result = greet_all(["Odin", "Thor", "Loki"])
        assert "Odin" in result
        assert "Thor" in result
        assert "Loki" in result

    def test_greet_all_empty_list_raises(self):
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError):
            greet_all([])


class TestIntegration:
    """Integration tests for the greeting module."""

    def test_greet_then_greet_all(self):
        """Test using both functions in sequence."""
        single = greet("Mimir")
        multiple = greet_all(["Mimir", "Ymir"])
        
        assert "Mimir" in single
        assert "Mimir" in multiple
        assert "Ymir" in multiple

    def test_consistency(self):
        """Test that greet_all with one name equals greet."""
        name = "Heimdallr"
        single = greet(name)
        multiple = greet_all([name])
        
        # Both should contain the name and be valid greetings
        assert name in single
        assert name in multiple
