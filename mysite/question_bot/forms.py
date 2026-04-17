from django import forms

class QuestionForm(forms.Form):
    question = forms.CharField(label='Question', max_length=256)

    def clean_question(self):
        question = self.cleaned_data['question'].strip()
        if not question.endswith('?'):
            raise forms.ValidationError("Tut tut tut! Someone's going to fail English! Use proper grammar and end your question with a question mark >:(.")
        if question and not question[0].isupper():
            raise forms.ValidationError("Tut tut tut! Someone's going to fail English! Use proper grammar and end your question with a question mark >:(.")
        return question