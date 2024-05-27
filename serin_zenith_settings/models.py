from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField


class InstructionTemplate(models.Model):
    name = models.CharField(max_length=100)
    instruct_template = HTMLField(blank=True, null=True)
    chat_template = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Grammar(models.Model):
    name = models.CharField(max_length=100)
    grammar = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.name


class CUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=100)
    cuser = models.ForeignKey(CUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars')
    greeting = HTMLField(blank=True, null=True)
    context = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Prompt(models.Model):
    name = models.CharField(max_length=100)
    prompt = HTMLField(blank=True, null=True)

    def __str__(self):
        return self.name


class GenerationSettings(models.Model):
    max_new_tokens = models.IntegerField(default=512,
                                         help_text="Maximum number of tokens to generate in a single request.")
    temperature = models.FloatField(default=0.7,
                                    help_text="Sampling temperature. Higher values make the output more random.")
    top_p = models.FloatField(default=0.9,
                              help_text="Nucleus sampling parameter. Only the tokens with top_p cumulative probability mass are considered.")
    top_k = models.IntegerField(default=20,
                                help_text="Number of highest probability vocabulary tokens to keep for top-k sampling.")
    typical_p = models.FloatField(default=1,
                                  help_text="Typical sampling parameter for nucleus sampling. Adjusting this value controls the diversity of the output.")
    min_p = models.FloatField(default=0,
                              help_text="Minimum value for dynamic temperature scaling. Increasing this value reduces the range of temperature fluctuations.")
    do_sample = models.BooleanField(default=True,
                                    help_text="Enable or disable sampling during text generation. Disabling this makes the output deterministic.")
    seed = models.IntegerField(default=-1,
                               help_text="Seed value for random number generation, enabling reproducibility of results. A fixed seed value ensures the same output for the same input.")
    max_tokens_second = models.IntegerField(default=0,
                                            help_text="Maximum number of tokens generated per second. Lower values throttle the generation speed.")
    skip_special_tokens = models.BooleanField(default=True,
                                              help_text="Skip special tokens in the output to maintain natural text flow. Enabling this ensures a cleaner output without special characters.")

    def __str__(self):
        return f'GenerationSettings (temperature: {self.temperature} max_new_tokens: {self.max_new_tokens})'


class SamplingParameters(models.Model):
    top_a = models.FloatField(default=0,
                              help_text="Top A sampling parameter, which controls the likelihood of token selection. Increasing this value focuses on more probable tokens.")
    smoothing_factor = models.FloatField(default=0,
                                         help_text="Factor used to smooth the output probabilities. Higher values result in smoother and less random outputs.")
    smoothing_curve = models.FloatField(default=1,
                                        help_text="Curve parameter for smoothing the output. Adjusting this value changes the steepness of the smoothing curve.")
    dynamic_temperature = models.BooleanField(default=False,
                                              help_text="Enable or disable dynamic temperature scaling. When enabled, temperature adjusts during generation based on context.")
    temperature_last = models.BooleanField(default=False,
                                           help_text="Apply temperature scaling as the final step during generation. Enabling this can make the output more stable.")
    auto_max_new_tokens = models.BooleanField(default=False,
                                              help_text="Automatically adjust the maximum number of new tokens generated. Enabling this allows dynamic adjustment based on the context.")
    custom_token_bans = models.TextField(blank=True, default='',
                                         help_text="Custom list of tokens to be banned during generation, in JSON format. Specifying tokens here ensures they are not generated.")
    sampler_priority = models.TextField(null=True, blank=True,
                                        help_text="Priority list of sampling techniques to be used during generation. Adjusting the order changes the sampling behavior.")

    def __str__(self):
        return f'SamplingParameters (top_a: {self.top_a}, dynamic_temperature: {self.dynamic_temperature})'


class PenaltiesAndFilters(models.Model):
    repetition_penalty = models.FloatField(default=1.15,
                                           help_text="Penalty applied to repeated tokens to reduce their likelihood. Increasing this value decreases the likelihood of repetitive outputs.")
    frequency_penalty = models.FloatField(default=0,
                                          help_text="Penalty for frequent tokens to reduce their likelihood of being chosen.")
    presence_penalty = models.FloatField(default=0,
                                         help_text="Penalty for presence of tokens to reduce their likelihood of being chosen.")
    repetition_penalty_range = models.IntegerField(default=1024,
                                                   help_text="Range of tokens to which the repetition penalty is applied. A larger range applies the penalty to more tokens.")
    penalty_alpha = models.FloatField(default=0,
                                      help_text="Alpha value for controlling the strength of the penalty applied to repeated tokens. Higher values increase the penalty strength.")
    encoder_repetition_penalty = models.FloatField(default=1,
                                                   help_text="Penalty applied to repeated tokens in the encoder. Higher values reduce the likelihood of repetitive sequences in the encoder.")
    no_repeat_ngram_size = models.IntegerField(default=0,
                                               help_text="Size of n-grams that are not allowed to repeat in the generated text. Increasing this value reduces repetitive phrases.")

    def __str__(self):
        return f'PenaltiesAndFilters (repetition_penalty: {self.repetition_penalty}, frequency_penalty: {self.frequency_penalty})'


class DynamicAdjustments(models.Model):
    dynatemp_low = models.FloatField(default=1,
                                     help_text="Lower bound for dynamic temperature scaling. A lower value increases variability in generation.")
    dynatemp_high = models.FloatField(default=1,
                                      help_text="Upper bound for dynamic temperature scaling. A higher value decreases variability in generation.")
    dynatemp_exponent = models.FloatField(default=1,
                                          help_text="Exponent value used in dynamic temperature scaling calculations. Increasing this value makes the temperature adjustment more aggressive.")
    mirostat_mode = models.IntegerField(default=0,
                                        help_text="Mode for Mirostat algorithm, which dynamically adjusts the temperature during generation. Different modes offer varying levels of control over temperature adjustment.")
    mirostat_tau = models.FloatField(default=5,
                                     help_text="Tau parameter for the Mirostat algorithm, controlling the learning rate for temperature adjustment. Higher values make the temperature adjustment more responsive.")
    mirostat_eta = models.FloatField(default=0.1,
                                     help_text="Eta parameter for the Mirostat algorithm, which influences the rate of convergence. Higher values result in faster convergence.")

    def __str__(self):
        return f'DynamicAdjustments (dynatemp_low: {self.dynatemp_low}, mirostat_mode: {self.mirostat_mode})'


class AdvancedSettings(models.Model):
    guidance_scale = models.FloatField(default=1,
                                       help_text="Scale factor for controlling the influence of guidance during generation. Higher values increase the influence of guidance.")
    negative_prompt = models.TextField(blank=True, default='',
                                       help_text="Text used to negatively influence the generation, reducing the likelihood of certain outputs. More negative prompts result in more filtered outputs.")
    epsilon_cutoff = models.FloatField(default=0,
                                       help_text="Cutoff for epsilon-based sampling, which removes tokens below a certain probability threshold. Higher values filter out more low-probability tokens.")
    eta_cutoff = models.FloatField(default=0,
                                   help_text="Cutoff for eta-based sampling, which adjusts token probabilities based on their ranks. Higher values make the generation more focused on high-ranked tokens.")

    def __str__(self):
        return f'AdvancedSettings (guidance_scale: {self.guidance_scale}, epsilon_cutoff: {self.epsilon_cutoff})'


class ContextualSettings(models.Model):
    truncation_length = models.IntegerField(default=0,
                                            help_text="Maximum length of the generated text after which truncation is applied. Lower values result in shorter outputs.")
    prompt_lookup_num_tokens = models.IntegerField(default=0,
                                                   help_text="Number of tokens used for prompt lookup in the context. Higher values provide more context to the model.")
    add_bos_token = models.BooleanField(default=True,
                                        help_text="Add a beginning-of-sequence token at the start of the input. Enabling this helps the model understand the start of the sequence.")
    ban_eos_token = models.BooleanField(default=False,
                                        help_text="Ban the end-of-sequence token to prevent premature termination of generation. Enabling this ensures the generation continues until manually stopped.")
    grammar_string = models.TextField(blank=True, default='',
                                      help_text="Grammar string for the model to enforce specific grammatical rules during generation. Specifying grammar rules ensures structured outputs.")

    def __str__(self):
        return f'ContextualSettings (truncation_length: {self.truncation_length}, add_bos_token: {self.add_bos_token})'


class TextGeneration(models.Model):
    preset = models.CharField(max_length=255, null=True, blank=True,
                              help_text="The name of a file under text-generation-webui/presets (without the .yaml extension). This file contains sampling parameters for generation.")
    generation_settings = models.ForeignKey(GenerationSettings, on_delete=models.CASCADE)
    sampling_parameters = models.ForeignKey(SamplingParameters, on_delete=models.CASCADE)
    penalties_and_filters = models.ForeignKey(PenaltiesAndFilters, on_delete=models.CASCADE)
    dynamic_adjustments = models.ForeignKey(DynamicAdjustments, on_delete=models.CASCADE)
    advanced_settings = models.ForeignKey(AdvancedSettings, on_delete=models.CASCADE)
    contextual_settings = models.ForeignKey(ContextualSettings, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f'{self.preset}, '
            f'TextGeneration (GenerationSettings: {self.generation_settings}, '
            f'SamplingParameters: {self.sampling_parameters}, '
            f'PenaltiesAndFilters: {self.penalties_and_filters}, '
            f'DynamicAdjustments: {self.dynamic_adjustments}, '
            f'AdvancedSettings: {self.advanced_settings}, '
            f'ContextualSettings: {self.contextual_settings})'
        )
