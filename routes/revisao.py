from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, CicloRevisao, IndicadorDado
from datetime import datetime

revisao_bp = Blueprint('revisao', __name__, url_prefix='/revisao')


@revisao_bp.route('/<token>', methods=['GET'])
def form(token):
    ciclo = CicloRevisao.query.filter_by(token=token).first()
    if not ciclo:
        flash('Link de revisão não encontrado.', 'danger')
        return redirect(url_for('gestao.index'))

    if ciclo.estado == 'revisto':
        return render_template('revisao/ja_revisto.html', ciclo=ciclo)

    indicadores_por_grupo = {}
    for ind in ciclo.indicadores:
        if ind.grupo not in indicadores_por_grupo:
            indicadores_por_grupo[ind.grupo] = []
        indicadores_por_grupo[ind.grupo].append(ind)

    return render_template(
        'revisao/form.html',
        ciclo=ciclo,
        indicadores_por_grupo=indicadores_por_grupo
    )


@revisao_bp.route('/<token>/submeter', methods=['POST'])
def submeter(token):
    ciclo = CicloRevisao.query.filter_by(token=token).first()
    if not ciclo:
        flash('Link de revisão não encontrado.', 'danger')
        return redirect(url_for('gestao.index'))

    if ciclo.estado == 'revisto':
        flash('Esta revisão já foi submetida.', 'warning')
        return redirect(url_for('revisao.form', token=token))

    nome_director = request.form.get('nome_director', '').strip()
    observacoes_director = request.form.get('observacoes_director', '').strip()

    if not nome_director:
        flash('Nome do director é obrigatório.', 'danger')
        return redirect(url_for('revisao.form', token=token))

    for ind in ciclo.indicadores:
        confirmado = request.form.get(f'confirmado_{ind.id}') == 'on'
        propor_eliminacao = request.form.get(f'propor_eliminacao_{ind.id}') == 'on'
        nome_editado = request.form.get(f'nome_editado_{ind.id}', '').strip()
        meta_editada = request.form.get(f'meta_editada_{ind.id}', '').strip()
        notas_director = request.form.get(f'notas_director_{ind.id}', '').strip()
        justificacao_eliminacao = request.form.get(f'justificacao_eliminacao_{ind.id}', '').strip()

        if propor_eliminacao and not justificacao_eliminacao:
            flash(f'Justificação obrigatória para eliminação do indicador {ind.codigo}.', 'danger')
            return redirect(url_for('revisao.form', token=token))

        ind.confirmado = confirmado
        ind.propor_eliminacao = propor_eliminacao
        ind.nome_editado = nome_editado if nome_editado else None
        ind.meta_editada = meta_editada if meta_editada else None
        ind.notas_director = notas_director if notas_director else None
        ind.justificacao_eliminacao = justificacao_eliminacao if justificacao_eliminacao else None

    ciclo.estado = 'revisto'
    ciclo.nome_director = nome_director
    ciclo.observacoes_director = observacoes_director
    ciclo.data_revisao = datetime.utcnow()

    db.session.commit()
    flash('Revisão submetida com sucesso!', 'success')
    return redirect(url_for('revisao.obrigado', token=token))


@revisao_bp.route('/<token>/obrigado', methods=['GET'])
def obrigado(token):
    ciclo = CicloRevisao.query.filter_by(token=token).first()
    if not ciclo or ciclo.estado != 'revisto':
        return redirect(url_for('revisao.form', token=token))

    return render_template('revisao/obrigado.html', ciclo=ciclo)
