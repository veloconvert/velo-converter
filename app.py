# --- GOOGLE SEARCH CONSOLE VERIFICATION (FORCE HEAD INJECTION) ---
# UYARI: Bu satır en tepede, set_page_config'den hemen sonra kalmalıdır.
st.components.v1.html(
    """
    <script>
        var meta = document.createElement('meta');
        meta.name = "google-site-verification";
        meta.content = "7QSo9l_GthJCi86IIW0CLwarA2KK0AtgZO-WN4PnlTE";
        parent.document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    height=0,
)
