from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.html import format_html, format_html_join

from .models import ApprovedImportedPublication, ApprovedReleaseInstallation, RegulationDraft, RegulatoryPublication, validate_payload
from .engine import ComplianceEngine


class DraftReviewForm(forms.ModelForm):
    sources_checked = forms.BooleanField(
        required=False,
        label="I have personally checked the linked official sources, dates, area restrictions and exceptions",
        help_text="Required for Publish reviewed revision. Saving a draft does not publish it.",
    )
    review_notes = forms.CharField(required=False, widget=forms.Textarea,
                                  help_text="Record what you checked and any remaining limitations.")

    class Meta:
        model = RegulationDraft
        fields = "__all__"


@admin.register(RegulationDraft)
class RegulationDraftAdmin(admin.ModelAdmin):
    form = DraftReviewForm
    list_display = ["title", "species", "land_type", "updated_at", "published_revision"]
    list_filter = ["species", "land_type"]
    search_fields = ["title", "key"]
    readonly_fields = ["updated_at", "published_revision", "review_summary"]
    change_form_template = "admin/integration/regulationdraft/change_form.html"
    actions = ["withdraw_publication"]

    def has_publish_permission(self, request):
        return request.user.has_perm("integration.publish_regulationdraft")

    @admin.action(description="Withdraw selected drafts' current published answers", permissions=["publish"])
    def withdraw_publication(self, request, queryset):
        count = 0
        for draft in queryset:
            changed = draft.publications.filter(is_current=True).update(is_current=False)
            if changed:
                self.log_change(request, draft, "Withdrew current reviewed publication; preserved revision history.")
                count += 1
        self.message_user(request, f"Withdrew {count} publications. Their working drafts remain unpublished.", messages.SUCCESS)

    @admin.display(description="Review the dated rules and official sources")
    def review_summary(self, obj):
        if not obj or not isinstance(obj.payload, dict):
            return "Save a valid working draft to view its review summary."
        try:
            validate_payload(obj.payload)
        except ValidationError:
            return "This working draft is incomplete. Correct the validation errors before source review."
        sources = format_html_join("", '<li><a href="{}" target="_blank" rel="noopener noreferrer">{}</a> — source checked {}. {}</li>',
            ((source.get("url", ""), source.get("title", ""), source.get("checked_on", ""), source.get("evidence", ""))
             for source in obj.payload.get("sources", []) if isinstance(source, dict)))
        rules = format_html_join("", '<li><strong>{} / {}</strong><br>{}<br>Bag: {}<br>Licenses: {}<br>Methods: {}<br>{}</li>',
            ((rule.get("name", ""), rule.get("category", ""),
              "; ".join(ComplianceEngine.period_label(period) for period in rule.get("periods", []) if isinstance(period, dict)),
              rule.get("bag", ""), rule.get("licenses", ""), rule.get("methods", ""), "; ".join(rule.get("alerts", [])))
             for rule in obj.payload.get("rules", []) if isinstance(rule, dict)))
        return format_html("<h3>Official sources</h3><ul>{}</ul><h3>Rule summary</h3><ul>{}</ul>", sources, rules)

    @admin.display(description="Current reviewed revision")
    def published_revision(self, obj):
        row = obj.publications.filter(is_current=True).first() if obj and obj.pk else None
        return f"{row.revision}, {row.reviewed_at:%Y-%m-%d %H:%M}, {row.reviewed_by}" if row else "Draft only — not public"

    def get_form(self, request, obj=None, **kwargs):
        parent = super().get_form(request, obj, **kwargs)

        class ReviewForm(parent):
            def clean(self):
                data = super().clean()
                if "_publish" in request.POST:
                    if not request.user.has_perm("integration.publish_regulationdraft"):
                        raise forms.ValidationError("You do not have regulatory publication permission.")
                    if not data.get("sources_checked") or not data.get("review_notes", "").strip():
                        raise forms.ValidationError("Check the source acknowledgement and enter review notes before publishing.")
                return data

        return ReviewForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "_publish" in request.POST:
            obj.publish(reviewer=request.user, sources_checked=form.cleaned_data["sources_checked"],
                        review_notes=form.cleaned_data["review_notes"])
            self.message_user(request, "A source-reviewed immutable revision is now public.", messages.SUCCESS)

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        context = {"can_publish": request.user.has_perm("integration.publish_regulationdraft")}
        context.update(extra_context or {})
        return super().changeform_view(request, object_id, form_url, context)


@admin.register(RegulatoryPublication)
class RegulatoryPublicationAdmin(admin.ModelAdmin):
    list_display = ["draft", "revision", "reviewed_by", "reviewed_at", "is_current"]
    readonly_fields = ["draft", "revision", "snapshot", "reviewed_by", "reviewed_at", "review_notes", "is_current"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ApprovedReleaseInstallation)
class ApprovedReleaseInstallationAdmin(admin.ModelAdmin):
    list_display = ["release_id", "installed_at", "publications_added", "existing_publications_preserved"]
    readonly_fields = ["release_id", "sha256", "installed_at", "publications_added", "existing_publications_preserved"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ApprovedImportedPublication)
class ApprovedImportedPublicationAdmin(admin.ModelAdmin):
    list_display = ["release_id", "reviewed_at", "is_current"]
    readonly_fields = ["release_id", "sha256", "snapshot", "reviewed_at", "review_notes", "is_current"]
    actions = ["withdraw_approved_import"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm("integration.publish_regulationdraft"):
            actions.pop("withdraw_approved_import", None)
        return actions

    @admin.action(description="Withdraw selected approved teammate information")
    def withdraw_approved_import(self, request, queryset):
        if not request.user.has_perm("integration.publish_regulationdraft"):
            self.message_user(request, "Regulatory publication permission is required.", messages.ERROR)
            return
        for publication in queryset.filter(is_current=True):
            self.log_change(request, publication, "Withdrew approved teammate information; immutable history retained.")
        count = queryset.filter(is_current=True).update(is_current=False)
        self.message_user(request, f"Withdrew {count} approved teammate publication(s).", messages.SUCCESS)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

