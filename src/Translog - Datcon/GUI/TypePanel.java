/* TypePanel  class

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that redistribution of source code include
the following disclaimer in the documentation and/or other materials provided
with the distribution.

THIS SOFTWARE IS PROVIDED BY ITS CREATOR "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE CREATOR OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

package src.GUI;

import java.awt.Color;
import java.awt.Desktop;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JComponent;
import javax.swing.JFormattedTextField;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.border.LineBorder;

import src.Files.ConvertDat;
import src.Files.CsvWriter;
import src.Files.DatConLog;
import src.Files.FileBeingUsed;
import src.apps.DatCon;

public class TypePanel extends JPanel implements ActionListener, PropertyChangeListener, IDatConPanel  {

    private static final long serialVersionUID = 1L;

    DatCon datCon = null;

    public JRadioButton optButton = null;

    public JRadioButton fullButton = null;

    public TypePanel(DatCon datCon) {
        this.datCon = datCon;

        setLayout(new GridBagLayout());
        setBorder(new LineBorder(Color.BLACK, 1, true));
        setOpaque(true);

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.BOTH;
        gbc.anchor = GridBagConstraints.WEST;

        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.weightx = 1.0;
        gbc.gridwidth = 1;
        JLabel label = new JLabel("Тип");
        Font font = new Font("Verdana", Font.BOLD, 16);
        label.setFont(font);
        add(label, gbc);
        gbc.weightx = 0.5;
        gbc.gridwidth = 1;
        gbc.anchor = GridBagConstraints.WEST;

        gbc.gridx = 1;
        gbc.gridy = 2;
        optButton = new JRadioButton("Оптимизированный");
        optButton.addActionListener(this);
        add(optButton, gbc);

        gbc.gridx = 1;
        gbc.gridy = 3;
        gbc.gridwidth = 2;
        fullButton = new JRadioButton("Полный");
        fullButton.addActionListener(this);
        add(fullButton, gbc);
        gbc.gridwidth = 1;

        gbc.fill = GridBagConstraints.BOTH;

        //        setBorder(BorderFactory.createLineBorder(Color.RED));

    }

    public void reset() {
        optButton.setSelected(true);
        fullButton.setSelected(false);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        try {
            JComponent source = (JComponent) (e.getSource());
            if (source == fullButton) {
                optButton.setSelected(false);
            } else if (source == optButton) {
                fullButton.setSelected(false);
            }
        } catch (Exception exception) {
            DatConLog.Exception(exception);
        }
    }
    public void propertyChange(PropertyChangeEvent evt) {
        // never called
    }
    @Override
    public void setArgs(ConvertDat convertDat) {
        if(fullButton.isSelected())  {
            convertDat.TypeGo = "full";
        } else {
            convertDat.TypeGo = "opt";
        }
    }

    @Override
    public void createPrintStreams(String outDirName)
            throws FileBeingUsed, FileNotFoundException {
        // never called
    }

    @Override
    public void closePrintStreams() {
        // never called
    }

    @Override
    public void createFileNames(String flyFileNameRoot) {
        // never called
    }
}
