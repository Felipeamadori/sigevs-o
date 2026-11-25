package br.com.pdsars.sigevs.competency;

import br.com.pdsars.sigevs.dto.PremiseSubmissionDTO;
import br.com.pdsars.sigevs.dto.SubmissionData;
import br.com.pdsars.sigevs.exception.UnprocessableEntityException;
import br.com.pdsars.sigevs.model.AreaPremise;
import br.com.pdsars.sigevs.model.ResponseArea;
import br.com.pdsars.sigevs.model.SurveillanceCycleZone;
import br.com.pdsars.sigevs.repository.AreaPremiseRepository;
import br.com.pdsars.sigevs.repository.BarrierSubmissionRepository;
import br.com.pdsars.sigevs.repository.PremiseSubmissionRepository;
import br.com.pdsars.sigevs.repository.ResponseAreaRepository;
import br.com.pdsars.sigevs.repository.ResponseBarrierRepository;
import br.com.pdsars.sigevs.repository.ResponseConvokedUsersRepository;
import br.com.pdsars.sigevs.repository.ResponseSurveillanceCycleRepository;
import br.com.pdsars.sigevs.repository.ResponseTeamRepository;
import br.com.pdsars.sigevs.repository.SanitaryEventResponseRepository;
import br.com.pdsars.sigevs.service.SubmissionService;
import br.com.pdsars.sigevs.service.SysEventLoggerService;
import br.com.pdsars.sigevs.service.TemporaryPremiseService;
import br.com.pdsars.sigevs.service.integration.PlanilhasService;
import br.com.pdsars.sigevs.service.registration.UsuarioService;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;

/**
 * Unit tests for the SIGEVS-O axiom AX-SEQ-06 (collection time window): a
 * property submission is only accepted when its collection instant lies within
 * the time window [start date, end date] of the zone per cycle that contains
 * the operational area of the property; a zone without dates is open unless it
 * is closed. The rule is enforced by {@code SubmissionService} before any other
 * submission rule. All collaborators are mocked (no database).
 *
 * <p>To observe that a collection <em>passed</em> the window check without
 * mocking the whole submission flow, the property in area is marked as already
 * completed: the next rule then rejects the submission with a different
 * message, which proves the window check was satisfied.</p>
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class CollectionTimeWindowAxiomTest {

    private static final long AREA_PREMISE_ID = 10L;
    private static final String VISIT_CLOSED = "As visitas para esse Estabelecimento já foram encerradas.";

    @Mock private PlanilhasService planilhasService;
    @Mock private PremiseSubmissionRepository premiseSubmissionRepository;
    @Mock private BarrierSubmissionRepository barrierSubmissionRepository;
    @Mock private SysEventLoggerService sysEventLoggerService;
    @Mock private ResponseBarrierRepository responseBarrierRepository;
    @Mock private SanitaryEventResponseRepository sanitaryEventResponseRepository;
    @Mock private ResponseConvokedUsersRepository responseConvokedUsersRepository;
    @Mock private AreaPremiseRepository areaPremiseRepository;
    @Mock private ResponseTeamRepository responseTeamRepository;
    @Mock private TemporaryPremiseService temporaryPremiseService;
    @Mock private UsuarioService usuarioService;
    @Mock private ResponseSurveillanceCycleRepository responseSurveillanceCycleRepository;
    @Mock private ResponseAreaRepository responseAreaRepository;

    @InjectMocks private SubmissionService submissionService;

    private SurveillanceCycleZone zone;

    @BeforeEach
    void setUp() {
        zone = new SurveillanceCycleZone();
        ResponseArea area = new ResponseArea();
        area.setSurveillanceCycleZone(zone);
        AreaPremise areaPremise = new AreaPremise();
        areaPremise.setArea(area);
        areaPremise.setIsCompleted(true); // see class comment
        when(areaPremiseRepository.findById(AREA_PREMISE_ID)).thenReturn(Optional.of(areaPremise));
        when(usuarioService.getCurrentUserId()).thenReturn(1);
    }

    /** Window of the zone per cycle: 16 to 18 May 2025 (America/Sao_Paulo). */
    private void window() {
        zone.setStartDate(LocalDate.of(2025, 5, 16));
        zone.setEndDate(LocalDate.of(2025, 5, 18));
    }

    private UnprocessableEntityException submitAt(String collectionInstant) {
        PremiseSubmissionDTO external = new PremiseSubmissionDTO();
        external.setAreaPremiseId(AREA_PREMISE_ID);
        external.setTeamId(7L);
        SubmissionData<PremiseSubmissionDTO> data = new SubmissionData<>();
        data.setExternalData(external);
        data.setDataHoraApp(collectionInstant);
        return assertThrows(UnprocessableEntityException.class,
                () -> submissionService.savePremiseSubmission(data, List.of()));
    }

    @Test
    @DisplayName("AX-SEQ-06 — coleta antes do início da janela da zona é rejeitada")
    void rejectsCollectionBeforeWindow() {
        window();
        UnprocessableEntityException ex = submitAt("2025-05-15T20:00:00Z");
        assertTrue(ex.getMessage().contains("anterior ao início da zona"), ex.getMessage());
        verifyNoInteractions(planilhasService, premiseSubmissionRepository);
    }

    @Test
    @DisplayName("AX-SEQ-06 — coleta após o fim da janela da zona é rejeitada")
    void rejectsCollectionAfterWindow() {
        window();
        UnprocessableEntityException ex = submitAt("2025-05-19T12:00:00Z");
        assertTrue(ex.getMessage().contains("Coletas posteriores não são permitidas"), ex.getMessage());
        verifyNoInteractions(planilhasService, premiseSubmissionRepository);
    }

    @Test
    @DisplayName("AX-SEQ-06 — coleta dentro da janela passa pela regra da janela")
    void acceptsCollectionInsideWindow() {
        window();
        UnprocessableEntityException ex = submitAt("2025-05-17T14:00:00Z");
        assertTrue(ex.getMessage().equals(VISIT_CLOSED),
                "the window check passed and the next rule was reached: " + ex.getMessage());
    }

    @Test
    @DisplayName("AX-SEQ-06 — o último dia da janela é inclusivo (horário de São Paulo)")
    void endDateIsInclusive() {
        window();
        // 18 May 2025, 23:30 in America/Sao_Paulo (UTC-3) = 19 May 02:30 UTC
        UnprocessableEntityException ex = submitAt("2025-05-19T02:30:00Z");
        assertTrue(ex.getMessage().equals(VISIT_CLOSED), ex.getMessage());
    }

    @Test
    @DisplayName("AX-SEQ-06 — zona sem datas e fechada não aceita coletas")
    void closedZoneWithoutDatesRejects() {
        zone.setClosed(true);
        UnprocessableEntityException ex = submitAt("2025-05-17T14:00:00Z");
        assertTrue(ex.getMessage().contains("fechada para novas submissões"), ex.getMessage());
    }

    @Test
    @DisplayName("AX-SEQ-06 — zona sem datas e aberta não restringe a coleta")
    void openZoneWithoutDatesAccepts() {
        zone.setClosed(false);
        UnprocessableEntityException ex = submitAt("2025-05-17T14:00:00Z");
        assertTrue(ex.getMessage().equals(VISIT_CLOSED), ex.getMessage());
    }
}
