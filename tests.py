import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_add_multiple_choices_generates_incremental_ids():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    c3 = question.add_choice('c')

    assert [c.id for c in question.choices] == [1, 2, 3]
    assert c1.id == 1
    assert c2.id == 2
    assert c3.id == 3


def test_remove_choice_by_id_removes_choice():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_choice_by_id(1)

    assert [c.id for c in question.choices] == [2]
    assert question.choices[0].text == 'b'


def test_remove_choice_by_invalid_id_raises():
    question = Question(title='q1')
    question.add_choice('a')

    with pytest.raises(Exception, match='Invalid choice id'):
        question.remove_choice_by_id(99)


def test_remove_all_choices_clears_list():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')

    question.remove_all_choices()

    assert question.choices == []


def test_set_correct_choices_marks_correct_options():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.set_correct_choices([2, 3])

    correct_ids = [c.id for c in question.choices if c.is_correct]
    assert correct_ids == [2, 3]


def test_correct_selected_choices_exceed_max_selections_raises():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    error_msg = None
    try:
        question.correct_selected_choices([1, 2, 3])
    except Exception as exc:
        error_msg = str(exc)

    assert error_msg is not None
    assert 'Cannot select more than 2 choices' in error_msg


def test_choice_text_empty_raises_exception():
    question = Question(title='q1')
    error_msg = None
    try:
        question.add_choice('', False)
    except Exception as exc:
        error_msg = str(exc)

    assert error_msg is not None
    assert 'Text cannot be empty' in error_msg


def test_choice_text_too_long_raises_exception():
    question = Question(title='q1')
    error_msg = None
    try:
        question.add_choice('x' * 101)
    except Exception as exc:
        error_msg = str(exc)

    assert error_msg is not None
    assert 'Text cannot be longer than 100 characters' in error_msg

def test_create_question_with_invalid_points():
    error_msg = None
    try:
        Question(title='q1', points=0)
    except Exception as exc:
        error_msg = str(exc)

    assert error_msg is not None
    assert 'Points must be between 1 and 100' in error_msg

    error_msg = None
    try:
        Question(title='q1', points=101)
    except Exception as exc:
        error_msg = str(exc)

    assert error_msg is not None
    assert 'Points must be between 1 and 100' in error_msg

def test_correct_selected_choices_returns_only_selected_correct_ids():
    question = Question(title='q1', max_selections=2)
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.set_correct_choices([1, 3])

    result = question.correct_selected_choices([1, 2])

    assert result == [1]
