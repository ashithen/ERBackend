# import base64
# import os
# from google import genai
# from google.genai import types
#
# from app.core.config import settings
# from app.models.data_model import DocResultData
#
# # doc_process_prompt:str =
#
#
# def generate(doc_text: str) -> DocResultData:
#     client = genai.Client(
#         api_key=settings.gemini_api_key
#     )
#
#     model = settings.llm_model
#     contents = [
#         types.Content(
#             role="user",
#             parts=[
#                 types.Part.from_text(text=doc_text),
#             ],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         response_mime_type="text/plain",
#         system_instruction=[
#             types.Part.from_text(text="""{
#   \"system_prompt\": {
#     \"role\": \"assistant\",
#     \"objective\": \"Transform lecture content into memory-optimized learning materials using proven cognitive techniques\",
#     \"input_requirements\": {
#       \"source\": \"Markdown text from lecture PDF\",
#       \"content_types\": [\"concepts\", \"hierarchies\", \"relationships\", \"key_details\"]
#     },
#     \"output_requirements\": {
#       \"format\": \"strict JSON\",
#       \"components\": {
#         \"mindmap\": {
#           \"structure\": {
#             \"topics\": {
#               \"subtopics\": {
#                 \"points\": \"concise_key_concepts\"
#               }
#             }
#           },
#           \"optimization\": \"hierarchical_compression\"
#         },
#         \"long_answer_questions\": {
#           \"requirements\": {
#             \"question_type\": \"descriptive\",
#             \"focus\": \"conceptual_understanding\",
#             \"coverage\": \"all_main_topics\"
#           }
#         },
#         \"flash_quiz\": {
#           \"structure\": {
#             \"question\": \"clear_stem\",
#             \"options\": \"4_plausible_choices\",
#             \"answer\": {
#               \"correct\": \"correct option\",
#               \"explanation\": \"1-sentence_rationale\"
#             }
#           },
#           \"coverage\": \"all_topics\"
#         },
#         \"memory_enhancement\": {
#           \"techniques\": {
#             \"primary_methods\": [\"SEE_Principle\", \"Journey_Method\", \"Visualization_Association\"],
#             \"secondary_methods\": [\"Car_Method\", \"Body_Method\", \"Pegging\"],
#             \"implementation_rules\": [
#               \"convert_abstract_to_concrete_images\",
#               \"use_hyperbolic_exaggeration\",
#               \"engage_multisensory_associations\",
#               \"anchor_to_existing_knowledge\"
#             ]
#           },
#           \"output_format\": \"topic_name: enhanced_concept_description\"
#         }
#       }
#     },
#     \"processing_rules\": [
#       \"prioritize_conceptual_clarity_over_verbatim_recall\",
#       \"maintain_scientific_accuracy\",
#       \"implement_spaced_repetition_principles\",
#       \"validate_question_distribution\",
#       \"ensure_interleaved_practice_variants\"
#     ],
#     \"validation_checks\": {
#       \"mindmap\": \"hierarchy_depth ≤ 3\",
#       \"questions\": \"no_overlap_between_question_sets\",
#       \"quiz\": \"distractor_quality_check\"
#     }
#   }
# }
# """),
#         ],
#     )
#
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         print(chunk.text, end="")
#
