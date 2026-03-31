"""
Enhanced Bibliomantic Divination System
Maintains backward compatibility while adding rich traditional content
"""

import logging
from typing import Optional, Tuple, Dict, Any
try:
    from .enhanced_iching_core import IChingAdapter, EnhancedIChing
except ImportError:
    from enhanced_iching_core import IChingAdapter, EnhancedIChing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedBiblioManticDiviner:
    """Enhanced divination system with rich traditional content (changing lines, secondary hexagram)."""

    def __init__(self, use_enhanced: bool = True):
        self.iching = IChingAdapter()
        self.enhanced_engine = EnhancedIChing()
        self.use_enhanced = True
        logger.info("Enhanced BiblioMantic Divination System initialized")
    
    def divine_query_augmentation(self, original_query: str) -> Tuple[str, dict]:
        """Enhanced query augmentation with changing lines and contextual interpretation."""
        try:
            result = self.enhanced_engine.generate_enhanced_divination(original_query)
            hexagram = result['primary_hexagram']

            divination_info = {
                "hexagram_number": hexagram.number,
                "hexagram_name": hexagram.english_name,
                "interpretation": hexagram.general_meaning,
                "method": "enhanced_three_coin_traditional",
                "bibliomantic_approach": "dick_high_castle_enhanced",
                "changing_lines": result.get('changing_lines', []),
                "contextual": True
            }

            context = self.enhanced_engine.infer_context_from_query(original_query)
            contextual_interpretation = self.enhanced_engine.get_contextual_interpretation(
                hexagram.number, context
            )

            wisdom_text = f"I Ching Hexagram {hexagram.number} - {hexagram.english_name} ({hexagram.chinese_name} {hexagram.unicode_symbol}): {contextual_interpretation}"

            if result.get('changing_lines'):
                line_guidance = self.enhanced_engine.get_changing_line_guidance(
                    hexagram.number, result['changing_lines']
                )
                wisdom_text += f" Changing lines: {'; '.join(line_guidance)}"

            augmented_query = self._integrate_wisdom_with_query(wisdom_text, original_query)
            logger.info(f"Enhanced divination performed: Hexagram {divination_info['hexagram_number']} - {divination_info['hexagram_name']}")
            return augmented_query, divination_info

        except Exception as e:
            logger.error(f"Enhanced divination failed: {str(e)}")
            return original_query, {"error": str(e), "fallback": True}
    
    def _integrate_wisdom_with_query(self, wisdom_text: str, original_query: str) -> str:
        """Enhanced wisdom integration"""
        integration_template = (
            "Consider this ancient wisdom as context for your response: {wisdom}\n\n"
            "Now, regarding the following question or request: {query}"
        )
        
        return integration_template.format(
            wisdom=wisdom_text,
            query=original_query
        )
    
    def perform_simple_divination(self) -> dict:
        """Perform divination with traditional three-coin method and changing lines."""
        try:
            result = self.enhanced_engine.generate_enhanced_divination()
            hexagram = result['primary_hexagram']
            return {
                "success": True,
                "hexagram_number": hexagram.number,
                "hexagram_name": hexagram.english_name,
                "interpretation": hexagram.general_meaning,
                "formatted_text": f"I Ching Hexagram {hexagram.number} - {hexagram.english_name}: {hexagram.general_meaning}",
                "enhanced": True,
                "changing_lines": result.get('changing_lines', [])
            }
        except Exception as e:
            logger.error(f"Enhanced simple divination failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "fallback_wisdom": "The path forward requires inner contemplation and patient observation."
            }
    
    def perform_enhanced_consultation(self, query: str) -> str:
        """Enhanced consultation with full traditional content (judgment, image, changing lines)."""
        try:
            result = self.enhanced_engine.generate_enhanced_divination(query)
            return self._format_enhanced_consultation(result, query)
        except Exception as e:
            logger.error(f"Enhanced consultation failed: {str(e)}")
            return f"Enhanced consultation failed: {str(e)}"
    
    def _prevailing_line(self, changing_lines: list, line_values: list) -> str:
        """Return a description of the prevailing line per traditional rules."""
        n = len(changing_lines)
        if n == 0:
            return "None — read the primary hexagram as a whole."
        if n == 1:
            ln = changing_lines[0]
            return f"Line {ln} — the single changing line governs the reading."
        if n == 2:
            a, b = sorted(changing_lines)
            type_a = line_values[a - 1] if line_values and a <= len(line_values) else None
            type_b = line_values[b - 1] if line_values and b <= len(line_values) else None
            if type_a == type_b:  # both Six or both Nine
                return f"Line {b} (upper of the two changing lines — same type)."
            else:
                # The Six line (old yin, value 6) prevails
                six_line = a if type_a == 6 else b
                return f"Line {six_line} — the Six (old yin) line prevails when types differ."
        if n == 3:
            mid = sorted(changing_lines)[1]
            return f"Line {mid} (middle of the three changing lines)."
        if n == 4:
            all_lines = list(range(1, 7))
            non_changing = [l for l in all_lines if l not in changing_lines]
            upper_non = max(non_changing)
            return f"Line {upper_non} — upper non-changing line (of four changing)."
        if n == 5:
            all_lines = list(range(1, 7))
            non_changing = [l for l in all_lines if l not in changing_lines]
            only_non = non_changing[0]
            return f"Line {only_non} — the sole non-changing line governs."
        if n == 6:
            all_six = all(v == 6 for v in line_values) if line_values else False
            all_nine = all(v == 9 for v in line_values) if line_values else False
            if all_six:
                return "All Six — read both the Cast Hexagram and the Transformed Hexagram."
            if all_nine:
                return "All Nine — read both the Cast Hexagram and the Transformed Hexagram."
            return "None — read the transformed hexagram only (no single line governs)."
        return "None."

    def _format_enhanced_consultation(self, divination_result: Dict[str, Any], query: str) -> str:
        """Format enhanced consultation with full traditional elements"""
        hexagram = divination_result['primary_hexagram']
        changing_lines = divination_result.get('changing_lines', [])
        line_values = divination_result.get('line_values', [])
        resulting_hexagram = divination_result.get('resulting_hexagram')
        
        # Infer context for targeted guidance
        context = self.enhanced_engine.infer_context_from_query(query)
        
        result = f"🔮 **Enhanced Bibliomantic Consultation**\n\n"
        result += f"**Your Question:** {query}\n\n"
        
        # Enhanced hexagram presentation (use hex_unicode from adamblvck when available)
        symbol = getattr(hexagram, "hex_unicode", None) or hexagram.unicode_symbol
        result += f"**Oracle's Guidance - Hexagram {hexagram.number}: {hexagram.english_name}**\n"
        result += f"*{hexagram.chinese_name} {symbol}*\n\n"
        
        # Judgment and Image (core I Ching elements; use text/comments split when available)
        if getattr(hexagram, "judgment_text", None):
            result += f"**Judgment:** *{hexagram.judgment_text}*\n\n{hexagram.judgment_comments or ''}\n\n"
        else:
            result += f"**Judgment:** {hexagram.judgment}\n\n"
        if getattr(hexagram, "image_text", None):
            result += f"**Image:** *{hexagram.image_text}*\n\n{hexagram.image_comments or ''}\n\n"
        else:
            result += f"**Image:** {hexagram.image}\n\n"
        
        # Context-specific guidance
        if context != "general" and context in hexagram.interpretations:
            result += f"**{context.title()} Guidance:** {hexagram.interpretations[context]}\n\n"
        else:
            result += f"**General Meaning:** {hexagram.general_meaning}\n\n"
        
        # Changing lines guidance if present (use text/comments split when available)
        if changing_lines:
            result += f"**Changing Lines:** {', '.join(map(str, changing_lines))}\n\n"
            prevailing = self._prevailing_line(changing_lines, line_values)
            result += f"**Prevailing Line:** {prevailing}\n\n"
            line_texts = getattr(hexagram, "changing_line_texts", None)
            line_comments = getattr(hexagram, "changing_line_comments", None)
            for line_num in changing_lines:
                # Determine line type from casting values (6 = old yin, 9 = old yang)
                line_val = line_values[line_num - 1] if line_values and line_num <= len(line_values) else None
                if line_val == 6:
                    line_type = "Six (changing yin)"
                elif line_val == 9:
                    line_type = "Nine (changing yang)"
                else:
                    line_type = "changing"
                if line_texts and line_num in line_texts and line_comments and line_num in line_comments:
                    result += f"• **Line {line_num} — {line_type}:** *{line_texts[line_num]}*\n\n  {line_comments[line_num]}\n\n"
                else:
                    guidance = self.enhanced_engine.get_changing_line_guidance(hexagram.number, [line_num])
                    if guidance:
                        # Replace the plain "Line N:" prefix with the typed version
                        text = guidance[0]
                        prefix = f"Line {line_num}: "
                        if text.startswith(prefix):
                            text = text[len(prefix):]
                        result += f"• **Line {line_num} — {line_type}:** {text}\n"
                    else:
                        result += f"• **Line {line_num} — {line_type}:** Traditional interpretation\n"
            result += "\n"
            
            if resulting_hexagram:
                result += f"**Resulting Situation - Hexagram {resulting_hexagram.number}: {resulting_hexagram.english_name}**\n"
                result += f"*{resulting_hexagram.chinese_name} {resulting_hexagram.unicode_symbol}*\n\n"
                result += f"{resulting_hexagram.general_meaning}\n\n"
        
        # Trigram analysis
        upper_trigram = self.enhanced_engine.trigrams.get(hexagram.upper_trigram)
        lower_trigram = self.enhanced_engine.trigrams.get(hexagram.lower_trigram)
        
        if upper_trigram and lower_trigram:
            result += f"**Trigram Analysis:**\n"
            result += f"• Upper: {upper_trigram.name} ({upper_trigram.chinese_name}) - {upper_trigram.attribute}\n"
            result += f"• Lower: {lower_trigram.name} ({lower_trigram.chinese_name}) - {lower_trigram.attribute}\n\n"
        
        # Commentary
        if hexagram.commentary.get('wilhelm'):
            result += f"**Traditional Commentary:** {hexagram.commentary['wilhelm']}\n\n"
        
        # Bibliomantic context (maintains existing format)
        result += "**Bibliomantic Context:**\n"
        result += "This enhanced consultation follows Philip K. Dick's approach in \"The Man in the High Castle,\" "
        result += "now enriched with traditional I Ching elements including changing lines, trigram analysis, "
        result += "and contextual interpretations for deeper philosophical reflection.\n\n"
        
        return result
    
    def validate_query(self, query: str) -> bool:
        """Validate that a query is suitable for bibliomantic augmentation"""
        if not query or not isinstance(query, str):
            return False
        
        cleaned_query = query.strip()
        
        if len(cleaned_query) < 3:
            return False
        
        return True
    
    def get_divination_statistics(self) -> dict:
        """Enhanced statistics (changing lines, trigrams, etc.)."""
        return {
            "total_hexagrams": 64,
            "divination_method": "Enhanced Traditional I Ching three-coin method with changing lines",
            "randomness_source": "Python secrets module (cryptographically secure)",
            "bibliomantic_approach": "Philip K. Dick - The Man in the High Castle style (Enhanced)",
            "system_status": "operational",
            "enhanced_features": True,
            "changing_lines": True,
            "trigram_analysis": True,
            "contextual_interpretations": True,
            "traditional_commentaries": True,
            "unicode_symbols": True
        }

# Backward compatibility functions
def augment_query_with_divination(query: str) -> Tuple[str, dict]:
    """Enhanced compatibility function"""
    diviner = EnhancedBiblioManticDiviner()
    return diviner.divine_query_augmentation(query)

def perform_divination() -> dict:
    """Enhanced compatibility function"""
    diviner = EnhancedBiblioManticDiviner()
    return diviner.perform_simple_divination()
