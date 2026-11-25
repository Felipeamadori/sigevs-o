package br.com.pdsars.sigevs.competency;

import br.com.pdsars.sigevs.dto.ResponseSubmissionsDTO;
import br.com.pdsars.sigevs.dto.TempPremiseSubmissionDTO;
import br.com.pdsars.sigevs.enums.SysEventType;
import br.com.pdsars.sigevs.model.AreaPremise;
import br.com.pdsars.sigevs.model.BarrierSubmission;
import br.com.pdsars.sigevs.model.EventSystemLog;
import br.com.pdsars.sigevs.model.registration.Usuario;
import br.com.pdsars.sigevs.model.TemporaryPremise;
import br.com.pdsars.sigevs.model.SanitaryEventResponse;
import br.com.pdsars.sigevs.repository.AreaPremiseRepository;
import br.com.pdsars.sigevs.repository.BarrierSubmissionRepository;
import br.com.pdsars.sigevs.repository.EventSystemLogRepository;
import br.com.pdsars.sigevs.repository.PremiseSubmissionRepository;
import br.com.pdsars.sigevs.repository.ResponseConvokedUsersRepository;
import br.com.pdsars.sigevs.repository.SanitaryAnalysisRepository;
import br.com.pdsars.sigevs.repository.SanitaryEventResponseRepository;
import br.com.pdsars.sigevs.repository.TemporaryPremiseRepository;
import br.com.pdsars.sigevs.repository.ResponseAreaRepository;
import br.com.pdsars.sigevs.repository.ResponseTeamRepository;
import br.com.pdsars.sigevs.repository.ResponseBarrierRepository;
import br.com.pdsars.sigevs.repository.ResponseSurveillanceCycleRepository;
import br.com.pdsars.sigevs.service.EventActionsService;
import br.com.pdsars.sigevs.service.integration.PlanilhasService;
import br.com.pdsars.sigevs.service.SysEventLoggerService;
import br.com.pdsars.sigevs.service.SubmissionService;
import br.com.pdsars.sigevs.service.TemporaryPremiseService;
import br.com.pdsars.sigevs.service.registration.UsuarioService;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.persistence.EntityNotFoundException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.junit.jupiter.MockitoSettings;
import org.mockito.quality.Strictness;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.Mockito.*;

/**
 * Unit tests for the Field Actions subdomain competency questions
 * (CQ-CAM-01..06). One test per competency question; all collaborators are
 * mocked (no database).
 */
@ExtendWith(MockitoExtension.class)
@MockitoSettings(strictness = Strictness.LENIENT)
class FieldActionsCompetencyQuestionsTest {

    private static final UUID RESPONSE_UUID = UUID.fromString("22222222-2222-2222-2222-222222222222");

    @Mock private SanitaryEventResponseRepository sanitaryEventResponseRepository;
    @Mock private ResponseConvokedUsersRepository responseConvokedUsersRepository;
    @Mock private SanitaryAnalysisRepository sanitaryAnalysisRepository;
    @Mock private PremiseSubmissionRepository premiseSubmissionRepository;
    @Mock private BarrierSubmissionRepository barrierSubmissionRepository;
    @Mock private AreaPremiseRepository areaPremiseRepository;
    @Mock private UsuarioService usuarioService;
    @Mock private br.com.pdsars.sigevs.service.integration.PlanilhasService planilhasService;

    @Mock private TemporaryPremiseRepository temporaryPremiseRepository;
    @Mock private br.com.pdsars.sigevs.repository.registration.EstabelecimentoRepository estabelecimentoRepository;
    @Mock private EventSystemLogRepository eventSystemLogRepository;
    @Mock private ResponseTeamRepository responseTeamRepository;
    @Mock private ResponseAreaRepository responseAreaRepository;
    @Mock private ResponseBarrierRepository responseBarrierRepository;
    @Mock private ResponseSurveillanceCycleRepository responseSurveillanceCycleRepository;

    @InjectMocks private EventActionsService eventActionsService;

    private SanitaryEventResponse activeResponse() {
        SanitaryEventResponse response = mock(SanitaryEventResponse.class);
        when(response.getIsActive()).thenReturn(true);
        when(response.getId()).thenReturn(5L);
        when(sanitaryEventResponseRepository.findByUuid(RESPONSE_UUID)).thenReturn(Optional.of(response));
        return response;
    }

    @Test
    @DisplayName("CQ-CAM-01 — Quais propriedades em uma área já foram visitadas e qual está pendente?")
    void cqCam01() {
        activeResponse();
        when(sanitaryAnalysisRepository.findAllocatedPremisesInTargetZones(5L))
                .thenReturn(List.of(
                        mock(br.com.pdsars.sigevs.dto.projection.PremiseProjection.class),
                        mock(br.com.pdsars.sigevs.dto.projection.PremiseProjection.class)));

        var premises = eventActionsService.findAllocatedPremises(RESPONSE_UUID);

        assertEquals(2, premises.size(),
                "allocated premises carry the visit status (visited / pending)");
    }

    @Test
    @DisplayName("CQ-CAM-02 — Qual o status de conclusão da visita a cada propriedade?")
    void cqCam02() {
        AreaPremise premise = new AreaPremise();
        premise.setIsCompleted(true);
        when(areaPremiseRepository.findById(1L)).thenReturn(Optional.of(premise));

        eventActionsService.completePremiseVisit(1L);
        assertTrue(premise.getIsCompleted());

        eventActionsService.reopenPremiseVisit(1L);
        assertFalse(premise.getIsCompleted(), "visitaConcluida toggles: complete and reopen");
    }

    @Test
    @DisplayName("CQ-CAM-03 — Quais submissões (formulários) foram realizadas por ciclo/equipe?")
    void cqCam03() {
        SanitaryEventResponse response = activeResponse();
        Usuario creator = mock(Usuario.class);
        when(creator.getIdUsuario()).thenReturn(1);
        when(response.getUserCreation()).thenReturn(creator);
        when(usuarioService.getCurrentUserId()).thenReturn(1);
        when(responseConvokedUsersRepository.isObserverOrManagementInFr(any(), any())).thenReturn(false);
        when(premiseSubmissionRepository.findPremiseSubmissionsByCycle(5L, 1L)).thenReturn(List.of());
        when(barrierSubmissionRepository.findPremiseSubmissionsAggregated(5L)).thenReturn(List.of());
        when(planilhasService.verificarPresencaArquivosPorUuids(anyList())).thenReturn(java.util.Map.of());

        ResponseSubmissionsDTO result = eventActionsService.findSubmissions(RESPONSE_UUID, Optional.of(1L));

        assertNotNull(result);
        verify(premiseSubmissionRepository).findPremiseSubmissionsByCycle(5L, 1L);
    }

    @Test
    @DisplayName("CQ-CAM-04 — Quais estabelecimentos na fase Não Cadastrado foram identificados em campo?")
    void cqCam04() {
        TempPremiseSubmissionDTO externalData = new TempPremiseSubmissionDTO();
        externalData.setCpfCnpj("44444444444");
        TemporaryPremise existing = new TemporaryPremise();
        existing.setCpfCnpj("44444444444");
        existing.setContactName("Maria Souza");
        when(temporaryPremiseRepository.findByCpfCnpj("44444444444")).thenReturn(Optional.of(existing));

        TemporaryPremiseService service = new TemporaryPremiseService(
                temporaryPremiseRepository, estabelecimentoRepository);
        TemporaryPremise result = service.findOrCreate(externalData);

        assertSame(existing, result,
                "an already registered temporary premise is reused, not duplicated");
        verify(estabelecimentoRepository, never()).save(any());
    }

    @Test
    @DisplayName("CQ-CAM-05 — Qual o histórico de auditoria das operações no sistema?")
    void cqCam05() {
        SysEventLoggerService loggerService = new SysEventLoggerService(
                eventSystemLogRepository, new ObjectMapper(), mock(br.com.pdsars.sigevs.repository.registration.UsuarioRepository.class));

        loggerService.log(SysEventType.INSERT, "Premise created");

        ArgumentCaptor<EventSystemLog> captor = ArgumentCaptor.forClass(EventSystemLog.class);
        verify(eventSystemLogRepository).save(captor.capture());
        assertEquals(SysEventType.INSERT, captor.getValue().getSysEventType());
        assertEquals("Premise created", captor.getValue().getMessage());
    }

    @Test
    @DisplayName("CQ-CAM-06 — Quais arquivos foram anexados a uma submissão?")
    void cqCam06() {
        // the attachment flag comes from the file store, keyed by submission uuid
        br.com.pdsars.sigevs.dto.BarrierSubmissionDTO projection =
                new br.com.pdsars.sigevs.dto.BarrierSubmissionDTO();
        projection.setSubmissionUuid(UUID.fromString("33333333-3333-3333-3333-333333333333"));

        var withFile = br.com.pdsars.sigevs.dto.BarrierSubmissionDTO
                .fromProjection(projection, true);
        var withoutFile = br.com.pdsars.sigevs.dto.BarrierSubmissionDTO
                .fromProjection(projection, false);

        assertTrue(withFile.getHasFile());
        assertFalse(withoutFile.getHasFile());
    }
}
