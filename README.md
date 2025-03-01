# Spardosen Manager

Spardosen Manager ist ein Python-Programm, mit dem du den Kontostand deiner Spardose verwalten kannst. Die Anwendung bietet sowohl einen grafischen Modus (GUI) als auch einen textbasierten Modus (CLI) und speichert alle Einstellungen (Sprache, Währung, Theme, Fenstermodus) sowie den Kontostand.

## Download

Um das Projekt herunterzuladen, folge diesen Schritten:

1. Gehe auf die Seite: [https://github.com/mojelumi0/SpardosenManager](https://github.com/mojelumi0/SpardosenManager)
2. Klicke auf **"Code"** und dann auf **"Download ZIP"**.
3. Der ZIP-Ordner wird in deinem Download-Ordner gespeichert. Extrahiere ihn.
4. Nach dem Extrahieren findest du die Hauptdatei (`main.py`) im Ordner.

Stelle sicher, dass du Python installiert hast. Für die Bearbeitung empfehlen wir einen Editor wie Visual Studio Code.

## Anwendung verwenden

### Grafischer Modus (GUI)

1. Führe das Skript ohne Parameter aus, um den grafischen Modus zu starten.
2. Gib einen Betrag in das Eingabefeld ein.
3. Klicke auf "Geld einzahlen" oder "Geld auszahlen", um die jeweilige Aktion durchzuführen.
4. Der aktuelle Kontostand wird angezeigt und bei Änderungen sofort aktualisiert.
5. Ändere über das Menü "Einstellungen" (Theme, Sprache, Währung, Fenstermodus) deine persönlichen Einstellungen.

### Kommandozeilenmodus (CLI)

1. Führe das Skript mit dem Parameter `--cli` aus, um den textbasierten Modus zu starten.
2. Folge dem angezeigten Menü, um Geld einzuzahlen, auszuzahlen oder den aktuellen Kontostand anzuzeigen.

## Einstellungen

Alle Einstellungen werden in der Datei `settings.json` gespeichert, während der Kontostand in der Datei `spardose.txt` abgelegt wird. Diese Dateien befinden sich im gleichen Verzeichnis wie das Skript.

- **Sprache:** Wähle zwischen Deutsch und Englisch.
- **Währung:** Lege dein bevorzugtes Währungssymbol fest.
- **Theme:** Wechsle zwischen Dark- und Light-Mode.
- **Fenstermodus:** Setze den Fenstermodus auf Normal, Vollbild, Maximiert oder Minimiert (nur im GUI-Modus).

## Autoren

Dieses Projekt wurde von **mojelumi** erstellt.

## Mitwirkende

**Lukas** (~ derteddy0)
