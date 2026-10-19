package org.medstudy.mobile;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.graphics.Typeface;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.content.Context;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;
import android.net.Uri;

public class MainActivity extends Activity {
    private static final String PREFS = "medstudy_settings";
    private static final String URL_KEY = "app_url";
    private LinearLayout root;
    private WebView webView;
    private ProgressBar progress;
    private String appUrl = "";

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(10, 24, 44));
        getWindow().setNavigationBarColor(Color.rgb(10, 24, 44));
        appUrl = getSharedPreferences(PREFS, MODE_PRIVATE).getString(URL_KEY, "");
        if (state != null) appUrl = state.getString(URL_KEY, appUrl);
        if (isValidUrl(appUrl)) showWebView(); else showSetup();
    }

    private int dp(float value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }

    private TextView text(String value, int size, int color) {
        TextView v = new TextView(this);
        v.setText(value);
        v.setTextSize(size);
        v.setTextColor(color);
        return v;
    }

    private void baseLayout() {
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(24), dp(24), dp(24), dp(24));
        root.setBackgroundColor(Color.rgb(10, 24, 44));
        setContentView(root);
    }

    private void showSetup() {
        baseLayout();
        TextView brand = text("MedStudy", 32, Color.WHITE);
        brand.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        root.addView(brand);
        TextView subtitle = text("Medical Learning Studio · Android test build", 15, Color.rgb(173, 197, 222));
        LinearLayout.LayoutParams subParams = new LinearLayout.LayoutParams(-1, -2);
        subParams.topMargin = dp(8);
        root.addView(subtitle, subParams);

        TextView note = text("Connect to your deployed MedStudy website. The Android package is a secure WebView wrapper; the Streamlit app must be hosted online first.", 15, Color.WHITE);
        LinearLayout.LayoutParams noteParams = new LinearLayout.LayoutParams(-1, -2);
        noteParams.topMargin = dp(28);
        root.addView(note, noteParams);

        EditText urlField = new EditText(this);
        urlField.setSingleLine(true);
        urlField.setTextColor(Color.WHITE);
        urlField.setHintTextColor(Color.rgb(173, 197, 222));
        urlField.setHint("https://your-app-name.streamlit.app");
        urlField.setInputType(android.text.InputType.TYPE_CLASS_TEXT | android.text.InputType.TYPE_TEXT_VARIATION_URI);
        urlField.setText(appUrl);
        urlField.setSelectAllOnFocus(true);
        urlField.setPadding(dp(12), dp(12), dp(12), dp(12));
        LinearLayout.LayoutParams inputParams = new LinearLayout.LayoutParams(-1, -2);
        inputParams.topMargin = dp(16);
        root.addView(urlField, inputParams);

        Button open = new Button(this);
        open.setText("Open MedStudy");
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(-1, -2);
        btnParams.topMargin = dp(12);
        root.addView(open, btnParams);
        open.setOnClickListener(v -> {
            String entered = urlField.getText().toString().trim();
            if (!isValidUrl(entered)) {
                Toast.makeText(this, "Enter a valid HTTPS Streamlit app URL.", Toast.LENGTH_LONG).show();
                return;
            }
            appUrl = entered;
            getSharedPreferences(PREFS, MODE_PRIVATE).edit().putString(URL_KEY, appUrl).apply();
            ((InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE))
                    .hideSoftInputFromWindow(urlField.getWindowToken(), 0);
            showWebView();
        });

        TextView help = text("Where to get the URL: deploy repository culprit-k/MedStudy, branch main, file app.py, using Streamlit Community Cloud. This screen does not deploy the server for you.", 13, Color.rgb(173, 197, 222));
        LinearLayout.LayoutParams helpParams = new LinearLayout.LayoutParams(-1, -2);
        helpParams.topMargin = dp(20);
        root.addView(help, helpParams);
    }

    private boolean isValidUrl(String value) {
        if (value == null || value.trim().isEmpty()) return false;
        Uri uri = Uri.parse(value.trim());
        return "https".equalsIgnoreCase(uri.getScheme()) && uri.getHost() != null;
    }

    private void showWebView() {
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(Color.WHITE);
        setContentView(root);

        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setOrientation(LinearLayout.HORIZONTAL);
        toolbar.setPadding(dp(8), dp(4), dp(8), dp(4));
        toolbar.setBackgroundColor(Color.rgb(10, 24, 44));
        Button back = new Button(this);
        back.setText("Back");
        toolbar.addView(back, new LinearLayout.LayoutParams(-2, -2));
        Button reconnect = new Button(this);
        reconnect.setText("Reload");
        toolbar.addView(reconnect, new LinearLayout.LayoutParams(-2, -2));
        Button settings = new Button(this);
        settings.setText("URL");
        toolbar.addView(settings, new LinearLayout.LayoutParams(-2, -2));
        root.addView(toolbar);

        progress = new ProgressBar(this, null, android.R.attr.progressBarStyleHorizontal);
        progress.setMax(100);
        root.addView(progress, new LinearLayout.LayoutParams(-1, dp(3)));

        webView = new WebView(this);
        webView.setBackgroundColor(Color.WHITE);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setSupportZoom(true);
        webView.getSettings().setBuiltInZoomControls(true);
        webView.getSettings().setDisplayZoomControls(false);
        webView.getSettings().setAllowFileAccess(false);
        webView.getSettings().setAllowContentAccess(false);
        webView.setWebChromeClient(new WebChromeClient() {
            @Override public void onProgressChanged(WebView view, int newProgress) {
                progress.setProgress(newProgress);
                progress.setVisibility(newProgress >= 100 ? View.GONE : View.VISIBLE);
            }
        });
        webView.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if ("https".equalsIgnoreCase(uri.getScheme())) return false;
                Toast.makeText(MainActivity.this, "Blocked non-HTTPS navigation.", Toast.LENGTH_SHORT).show();
                return true;
            }
        });
        root.addView(webView, new LinearLayout.LayoutParams(-1, 0, 1));
        back.setOnClickListener(v -> {
            if (webView.canGoBack()) webView.goBack(); else showSetup();
        });
        reconnect.setOnClickListener(v -> webView.reload());
        settings.setOnClickListener(v -> showSetup());
        webView.loadUrl(appUrl);
    }

    @Override public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else showSetup();
    }

    @Override protected void onSaveInstanceState(Bundle outState) {
        outState.putString(URL_KEY, appUrl);
        super.onSaveInstanceState(outState);
    }

    @Override protected void onDestroy() {
        if (webView != null) {
            webView.stopLoading();
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}
