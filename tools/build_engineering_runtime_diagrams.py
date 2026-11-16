"""Generate bilingual engineering and runtime architecture diagrams."""
from pathlib import Path
from tools.build_agent_diagrams import base, box, arrow, chips, text
from tools.build_agent_social import font
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'engineering-runtime'

def render(kind, es):
    if kind == 'tracks':
        p = base('Dos caminos' if es else 'Two tracks', 'La relación es condicional' if es else 'The relationship is conditional')
        p += [box(110, 'Ingeniería asistida por IA' if es else 'AI-assisted engineering', 'Personas + agentes + CI' if es else 'People + agents + CI', height=100), arrow(210,250), box(252, 'Software entregado' if es else 'Delivered software', 'API convencional o producto con IA' if es else 'Conventional API or AI product', height=100), arrow(352,392), box(394, '¿Usa IA al ejecutarse?' if es else 'Does it use AI at runtime?', height=90, accent='#e2b977'), chips(510, ['No → sin inferencia' if es else 'No → no inference', 'Sí → controles IA' if es else 'Yes → AI controls'], height=80), box(650, 'Capacidades compartidas' if es else 'Shared capabilities', 'Políticas y responsables distintos' if es else 'Different policies and owners', height=100, accent='#8bbca7')]
    elif kind == 'boundaries':
        p = base('Límites de confianza' if es else 'Trust boundaries', 'La autoridad cambia con el contexto' if es else 'Authority depends on context')
        p += [box(105, 'Developer → coding agent', 'Identidad y permisos delegados' if es else 'Delegated identity and permissions', height=94), arrow(199,228), box(230, 'Repositorio + herramientas' if es else 'Repository + tools', 'Cambios → CI → revisión' if es else 'Changes → CI → review', height=94), text(240,375,'LÍMITE DE ENTREGA' if es else 'DELIVERY BOUNDARY',18,color='#e2b977'), box(414, 'Aplicación → agente' if es else 'Application → agent', 'Identidad de servicio' if es else 'Service identity', height=94,accent='#8bbca7'), arrow(508,537), box(539, 'Datos + herramientas de negocio' if es else 'Business data + tools', 'Tenant · autorización · aprobación' if es else 'Tenant · authorization · approval', height=100,accent='#8bbca7'), text(240,718,'Cada acción cruza un límite' if es else 'Each action crosses a boundary',18,color='#e2b977')]
    elif kind == 'shared':
        p = base('Capacidades compartidas' if es else 'Shared capabilities', 'Interfaces comunes, contratos distintos' if es else 'Common interfaces, different contracts')
        p += [chips(110,['Developers','Coding agents','Workflows','AI workloads'],height=66), arrow(252,286), chips(288,['Identidad' if es else 'Identity','Políticas' if es else 'Policy','Observabilidad' if es else 'Observability','Registro' if es else 'Registry','Evaluación' if es else 'Evaluation','Coste' if es else 'Cost'],height=66), arrow(516,550), box(552,'Contratos por consumidor' if es else 'Contracts per consumer','Permisos · límites · SLO' if es else 'Permissions · boundaries · SLOs',height=106,accent='#8bbca7'), text(240,730,'Compartir ≠ misma autoridad' if es else 'Sharing ≠ same authority',18,color='#e2b977')]
    else:
        p = base('Árbol de decisión' if es else 'Decision tree', 'Añadir controles según riesgo' if es else 'Add controls based on risk')
        p += [box(102,'¿IA en ejecución?' if es else 'AI at runtime?', 'No → controles de desarrollo' if es else 'No → engineering controls',height=100),arrow(202,228),box(230,'Sí → inferencia' if es else 'Yes → inference','Identidad · calidad · coste' if es else 'Identity · quality · cost',height=100),arrow(330,356),box(358,'¿RAG o herramientas?' if es else 'RAG or tools?','Datos, acceso y aislamiento' if es else 'Data, access and isolation',height=100,accent='#8bbca7'),arrow(458,484),box(486,'¿Acciones externas?' if es else 'External side effects?','Permisos · aprobación · recuperación' if es else 'Permissions · approval · recovery',height=100,accent='#e2b977'),arrow(586,612),box(614,'¿Compartido o alto riesgo?' if es else 'Shared or high risk?','Responsable · SLO · controles extra' if es else 'Owner · SLO · added controls',height=108)]
    return '\n'.join(p+['</svg>'])+'\n'

def build():
    for kind in ('tracks','boundaries','shared','decision'):
        for lang in ('en','es'):
            (ROOT/'assets/images/flows'/f'{PREFIX}-{kind}-{lang}.svg').write_text(render(kind,lang=='es'),encoding='utf-8')
    for lang, lines, sub in [('en',['AI-assisted engineering','and production AI'],'Two operating models. Shared capabilities.'),('es',['Ingeniería asistida por IA','e IA en producción'],'Dos modelos operativos. Capacidades compartidas.')]:
        image=Image.new('RGB',(1200,630),'#122031'); draw=ImageDraw.Draw(image)
        draw.rounded_rectangle((38,38,1162,592),radius=28,outline='#466b80',width=2)
        draw.text((88,81),'REINALDO LEÓN  /  WRITING',font=font(23),fill='#a9c4d5')
        for i,line in enumerate(lines): draw.text((88,190+i*84),line,font=font(52),fill='#f3f4f6')
        draw.text((88,465),sub,font=font(26),fill='#a9c4d5')
        image.save(ROOT/'assets/images/writing'/f'ai-assisted-engineering-vs-production-ai-runtime-{lang}.png',optimize=True)
if __name__ == '__main__': build()
