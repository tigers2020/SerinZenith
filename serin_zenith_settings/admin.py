from django.contrib import admin
from .models import (
    InstructionTemplate, Grammar, CUser, Character, Prompt, GenerationSettings,
    SamplingParameters, PenaltiesAndFilters, DynamicAdjustments, AdvancedSettings, ContextualSettings, TextGeneration
)


@admin.register(TextGeneration)
class TextGenerationAdmin(admin.ModelAdmin):
    list_display = (
        'preset', 'generation_settings', 'sampling_parameters', 'penalties_and_filters', 'dynamic_adjustments',
        'advanced_settings', 'contextual_settings')
    fields = ('preset', 'generation_settings', 'sampling_parameters', 'penalties_and_filters', 'dynamic_adjustments',
              'advanced_settings', 'contextual_settings')


@admin.register(GenerationSettings)
class GenerationSettingsAdmin(admin.ModelAdmin):
    list_display = (
        'max_new_tokens', 'temperature', 'top_p', 'top_k', 'typical_p', 'min_p', 'do_sample', 'seed',
        'max_tokens_second',
        'skip_special_tokens')
    fields = (
        'max_new_tokens', 'temperature', 'top_p', 'top_k', 'typical_p', 'min_p', 'do_sample', 'seed',
        'max_tokens_second',
        'skip_special_tokens')


@admin.register(SamplingParameters)
class SamplingParametersAdmin(admin.ModelAdmin):
    list_display = (
        'top_a', 'smoothing_factor', 'smoothing_curve', 'dynamic_temperature', 'temperature_last',
        'auto_max_new_tokens',
        'custom_token_bans', 'sampler_priority')
    fields = (
        'top_a', 'smoothing_factor', 'smoothing_curve', 'dynamic_temperature', 'temperature_last',
        'auto_max_new_tokens',
        'custom_token_bans', 'sampler_priority')


@admin.register(PenaltiesAndFilters)
class PenaltiesAndFiltersAdmin(admin.ModelAdmin):
    list_display = (
        'repetition_penalty', 'frequency_penalty', 'presence_penalty', 'repetition_penalty_range', 'penalty_alpha',
        'encoder_repetition_penalty', 'no_repeat_ngram_size')
    fields = (
        'repetition_penalty', 'frequency_penalty', 'presence_penalty', 'repetition_penalty_range', 'penalty_alpha',
        'encoder_repetition_penalty', 'no_repeat_ngram_size')


@admin.register(DynamicAdjustments)
class DynamicAdjustmentsAdmin(admin.ModelAdmin):
    list_display = (
        'dynatemp_low', 'dynatemp_high', 'dynatemp_exponent', 'mirostat_mode', 'mirostat_tau', 'mirostat_eta')
    fields = ('dynatemp_low', 'dynatemp_high', 'dynatemp_exponent', 'mirostat_mode', 'mirostat_tau', 'mirostat_eta')


@admin.register(AdvancedSettings)
class AdvancedSettingsAdmin(admin.ModelAdmin):
    list_display = ('guidance_scale', 'negative_prompt', 'epsilon_cutoff', 'eta_cutoff')
    fields = ('guidance_scale', 'negative_prompt', 'epsilon_cutoff', 'eta_cutoff')


@admin.register(ContextualSettings)
class ContextualSettingsAdmin(admin.ModelAdmin):
    list_display = ('truncation_length', 'prompt_lookup_num_tokens', 'add_bos_token', 'ban_eos_token', 'grammar_string')
    fields = ('truncation_length', 'prompt_lookup_num_tokens', 'add_bos_token', 'ban_eos_token', 'grammar_string')


admin.site.register(InstructionTemplate)
admin.site.register(Grammar)
admin.site.register(CUser)
admin.site.register(Character)
admin.site.register(Prompt)
